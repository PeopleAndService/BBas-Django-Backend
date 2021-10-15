from datetime import time, timezone
from enum import Flag
from typing import OrderedDict
from django.shortcuts import render

from django.http.response import HttpResponse, JsonResponse
from drf_yasg.openapi import Response
from requests.api import head
from rest_framework.parsers import JSONParser 
from rest_framework import serializers, status

from .models import QueueData, PassengerAccount, DriverAccount, RatingData, busStationData, routePerBus, routeData
from .serializers import DriverSerializer, PassengerSerializer, QueueSerializer, RatingSerializer, busSerializer, routeBusStationSerializer, routeSerializer
from rest_framework.decorators import api_view
from rest_framework import generics

from haversine import haversine

import requests
import datetime
import urllib.request
import json
import time

postFlag = False # 메시지를 보냈는지 진리 값 변수
recentNodeId = "" # 최근 queue에 올린 데이터의 nodeId 변수
recentVehicleId = "" # 최근 queue에 올린 데이터의 vehicleID 변수
recentPostMan = "" # queue에 데이터를 올린 사용자 uid 변수
recentCheck = True #최근에 포스트를 했는지 진리 값 변수
recentMessageMan = "" #최근에 기사에게 메시지를 보낸 사용자 uid 변수

# Queue데이터 API

@api_view(['GET','POST','PUT','DELETE'])
def queue(request,slug):       #Queue데이터 등록, 반환, 삭제, 업데이트 API
    try:
        qData = QueueData.objects
    except QueueData.DoesNotExist:
            return JsonResponse({'success':False, 'result': {}}, status=status.HTTP_404_NOT_FOUND)
    
    if (request.method == 'POST'):
        parsed_data = JSONParser().parse(request)
        q_serializer = QueueSerializer(data = parsed_data)
        if q_serializer.is_valid():
            q_serializer.save()
            check_QueuePosting(parsed_data['stbusStopId'], parsed_data['vehicleId'], parsed_data['uid'])
            return JsonResponse({'success':True, 'result': q_serializer.data}, status = status.HTTP_201_CREATED)
        else:
            print(q_serializer.errors)
            return JsonResponse({'success':False, 'result': {}}, status = status.HTTP_400_BAD_REQUEST)

    elif (request.method == 'GET'):
        if slug ==  "0" :
            q_serializer = QueueSerializer(qData.all(), many=True)
            return JsonResponse({'success':True,'result' : q_serializer.data}, status=status.HTTP_200_OK)
        else :
            filtered_data = qData.filter(uid = slug)
            if len(filtered_data) == 0:
                return JsonResponse({'success':False, 'result':{}})
            else:
                tempRoute = filtered_data[0].busRouteId
                tempData = routeData.objects.filter(busRouteId = tempRoute)
                q_serializer = QueueSerializer(filtered_data, many = True)
                q_serializer.data[0]['destination'] =tempData[0].destination
                q_serializer.data[0]['routeNo'] = tempData[0].routeNo
            return JsonResponse({'success':True, 'result' : q_serializer.data[0]}, status = status.HTTP_200_OK)
    
    elif (request.method == 'PUT'):
        parsed_data = JSONParser().parse(request)
        filtered_data = qData.filter(uid = parsed_data['uid'])[0]
        parsed_data['stbusStopId'] = filtered_data.stbusStopId
        parsed_data['edbusStopId'] = filtered_data.edbusStopId
        parsed_data['stNodeOrder'] = filtered_data.stNodeOrder
        parsed_data['edNodeOrder'] = filtered_data.edNodeOrder
        parsed_data['vehicleId'] = filtered_data.vehicleId
        parsed_data['busRouteId'] = filtered_data.busRouteId
        q_serializer = QueueSerializer(filtered_data, data=parsed_data)
        tempDatas = routeData.objects.filter(busRouteId = filtered_data.busRouteId)
        tempData = dict()
        if q_serializer.is_valid():
            q_serializer.save()
            tempData = q_serializer.data
            tempData['destination']= tempDatas[0].destination
            tempData['routeNo'] = tempDatas[0].routeNo
            return JsonResponse({'success': True, 'result': tempData}, status= status.HTTP_200_OK)
        else:
            print(q_serializer.errors)
            return JsonResponse({'success': False, 'result': {}}, status=status.HTTP_400_BAD_REQUEST)

    elif (request.method == 'DELETE'):
        data = JSONParser().parse(request)
        if data['uid'] is not None :
            if (len(qData.filter(uid=data['uid']))==0):
                return JsonResponse({'success':False, 'result':{}}, status=status.HTTP_204_NO_CONTENT)
            else:
                filtered_data = qData.filter(uid = data['uid'])
                filtered_data.delete()
                return JsonResponse({'success' : True, 'result' : {}}, status=status.HTTP_200_OK)
        else :
            return JsonResponse({'success':False,'result' : {}}, status=status.HTTP_400_BAD_REQUEST)
    
#평가 데이터 API

@api_view(['GET','POST'])
def rating(request, slug):   # 평가 등록 API
    try:
        rData = RatingData.objects
        
    except RatingData.DoesNotExist:
            return JsonResponse({'success': False, 'result' : {}}, status = status.HTTP_404_NOT_FOUND)
            
    if (request.method == 'POST'):
        parsed_data = JSONParser().parse(request)
        dData = DriverAccount.objects.filter(vehicleId = parsed_data['vehicleId'])
        if len(dData) == 0:
            return JsonResponse({'success':False, 'result':{}}, status=status.HTTP_400_BAD_REQUEST)
        driverId = dData[0].did
        intpudData = {'ratingData': parsed_data['ratingData'], 'did': driverId}
        if len(rData.filter(did = driverId)) == 0:
            print("현재 평가 없음")
        else:
            temp = rData.filter(did = driverId)
            currentScore = temp[0].ratingData
            parsed_data['ratingData'] = parsed_data['ratingData'] + currentScore
        
        r_serializer = RatingSerializer(data = intpudData)
        if r_serializer.is_valid():
            r_serializer.save()
            return JsonResponse({'success':True, 'result' :{}}, status = status.HTTP_201_CREATED)
        else:
            print(r_serializer.errors)
            return JsonResponse({'success':False, 'result':{}}, status=status.HTTP_400_BAD_REQUEST)
    
    elif (request.method == 'GET'):
        if slug == "0" :
            r_serializer = RatingSerializer(rData.all(), many=True)
            return JsonResponse({'success':True,'result' : r_serializer.data}, status=status.HTTP_200_OK)    
        else :
            filtered_data = rData.filter(did = slug)
            r_serializer = RatingSerializer(filtered_data, many = True)
            return JsonResponse({'success':True, 'result' : r_serializer.data[0]}, status = status.HTTP_200_OK)
  

#사용자 데이터 API


@api_view(['POST', 'PUT', 'DELETE'])
def passengerByUid(request):                     #사용자의 uid를 받아서 반환, 업데이트, 삭제
    try:
        data = JSONParser().parse(request)
        passengerData = PassengerAccount.objects.filter(uid=data['uid'])
    except PassengerAccount.DoesNotExist:
        return JsonResponse({'success':False, 'result': {}},status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        if data['uid'] is not None:
            if len(passengerData) == 0 :
                return JsonResponse({'success':False,'result': {}}, safe=False, status = status.HTTP_204_NO_CONTENT)
            else:
                serializedData = PassengerSerializer(passengerData, many=True)
                return JsonResponse({'success':True,'result': serializedData.data[0]}, safe=False, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'success':False, 'result':{}},status=status.HTTP_400_BAD_REQUEST)
            
    elif (request.method == 'PUT'):
        if data['uid'] is not None:
            if len(passengerData) == 0 :
                return JsonResponse({'success':False,'result': {}}, safe=False, status=status.HTTP_204_NO_CONTENT)
            else:
                filtTmp = PassengerSerializer(passengerData, many=True)
                if "name" not in data:
                    data['name'] = filtTmp.data[0]['name']
                passengerData = passengerData.get()
                serializer = PassengerSerializer(passengerData,data = data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse({'success':True,'result': serializer.data}, safe=False, status=status.HTTP_200_OK)
                else:
                    return JsonResponse({'success':False,'result': {}}, safe=False, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({'success':False, 'result':{}},status=status.HTTP_400_BAD_REQUEST)

    elif (request.method == 'DELETE'):
        if data['uid'] is not None:
            if len(passengerData) == 0 :
                return JsonResponse({'success':False,'result': {}}, safe=False, status=status.HTTP_204_NO_CONTENT)
            else:
                filteredData = passengerData.filter(uid=data['uid'])
                filteredData.delete()
                return JsonResponse({'success':True, 'result':{}},status=status.HTTP_200_OK)
        else:
            return JsonResponse({'success':False, 'result':{}},status=status.HTTP_400_BAD_REQUEST)

#기사 Data API

@api_view(['POST', 'PUT', 'DELETE'])
def driverByUid(request):                     #기사의 did값을 받아서 반환, 업데이트, 삭제 API
    try:
        data = JSONParser().parse(request)
        driverData = DriverAccount.objects.filter(did=data['did'])
    except DriverAccount.DoesNotExist:
        return JsonResponse({'success':False, 'result': {}},status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        if data['did'] is not None:
            if len(driverData) == 0:
                return JsonResponse({'success':False,'result': {}}, safe=False, status=status.HTTP_204_NO_CONTENT)
            else:
                serializedData = DriverSerializer(driverData, many=True)
                return JsonResponse({'success':True,'result': serializedData.data[0]}, safe=False, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'success':False, 'result':{}},status=status.HTTP_400_BAD_REQUEST)

    elif (request.method == 'PUT'): #기사가 운전을 시작할 때 
        if data['did'] is not None:
            if len(driverData) == 0:
                return JsonResponse({'success':False,'result': {}}, safe=False, status=status.HTTP_204_NO_CONTENT)
            else:
                filtTmp = DriverSerializer(driverData, many=True)
                if "name" not in data:
                    data['name'] = filtTmp.data[0]['name']

                driverData = driverData.get()
                d_serializer = DriverSerializer(driverData, data=data)
                if d_serializer.is_valid():
                    
                    d_serializer.save()
                    return JsonResponse({'success':True,'result': d_serializer.data}, safe=False, status=status.HTTP_200_OK)
                else:
                    print(d_serializer.errors)
                    return JsonResponse({'success':False,'result': {}}, safe=False, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({'success':False, 'result':{}},status=status.HTTP_400_BAD_REQUEST)

    elif (request.method == 'DELETE'):
        if data['did'] is not None:
            if len(driverData) == 0:
                return JsonResponse({'success':False,'result': {}}, safe=False, status=status.HTTP_204_NO_CONTENT)
            else:
                filteredData = driverData.get()
                filteredData.delete()
                return JsonResponse({'success':True,'result':{}},status=status.HTTP_200_OK)
        else:
            return JsonResponse({'success':False,'result':{}},status=status.HTTP_400_BAD_REQUEST)


# 로그인 관련 API

@api_view(['POST'])
def passengerSign(request): #사용자 어플 로그인 APi
    try:
        passengerData = PassengerAccount.objects
        data = JSONParser().parse(request)
    except PassengerAccount.DoesNotExist:
        return JsonResponse({'success':False, 'result': {}},status=status.HTTP_404_NOT_FOUND)
    if (request.method == 'POST'):
        if data['uid'] is not None:
            if(len(passengerData.filter(uid = data['uid']))) != 0:
                filteredData = passengerData.filter(uid=data['uid'])
                serializer = PassengerSerializer(filteredData, many=True)
                return JsonResponse({"success" : True, "result": serializer.data[0]}, status=status.HTTP_202_ACCEPTED)
            elif(len(passengerData.filter(uid = data['uid']))) == 0:
                p_serializer = PassengerSerializer(data = data)
                if p_serializer.is_valid():
                    p_serializer.save()
                    return JsonResponse({'success': True, 'result':p_serializer.data}, status = status.HTTP_201_CREATED)
            else:
                return JsonResponse({'success': False, "result": {}}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return JsonResponse({'success' : False, "result": {}}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({'success' : False, "result": {}}, status=status.HTTP_403_FORBIDDEN)

@api_view(['POST'])
def driverSign(request): #기사 어플 로그인 API
    try:
        driverData = DriverAccount.objects
        data = JSONParser().parse(request)
    except DriverAccount.DoesNotExist:
        return JsonResponse({'success':False, 'result': {}},status=status.HTTP_404_NOT_FOUND)
    if (request.method == 'POST'):
        if data['did'] is not None:
            if(len(driverData.filter(did = data['did']))) != 0:
                filteredData = driverData.filter(did=data['did'])               
                serializer = DriverSerializer(filteredData, many=True)
                return JsonResponse({"success" : True, "result": serializer.data[0]}, status=status.HTTP_202_ACCEPTED)
            elif(len(driverData.filter(did = data['did']))) == 0:
                d_serializer = DriverSerializer(data = data)
                if d_serializer.is_valid():
                    d_serializer.save()
                    return JsonResponse({'success':True, 'result' : d_serializer.data}, status = status.HTTP_201_CREATED)
            else:
                return JsonResponse({'success' : False, "result": {}}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return JsonResponse({'success' : False, "result": {}}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({'success' : False, "result": {}}, status=status.HTTP_403_FORBIDDEN)
    
    # Data 호출 API
@api_view(['POST'])
def QueueInfo(request): # 기사에게 데이터를 주는 API
    if request.method == 'POST':
        global recentNodeId, recentVehicleId, recentPostMan, recentCheck, recentMessageMan
        data = JSONParser().parse(request)
        print(data)
        ordered = 0
        tempIndex = {'recentResult':{'stationName':"", 'queueTime':""}}
        url = "http://openapi.tago.go.kr/openapi/service/BusLcInfoInqireService/getRouteAcctoBusLcList?serviceKey=TGl%2FEQu3DnkXz1pe5Wyi3AveK9xofqEHe6zRAzkSH1DQ2eGsyOgiCp8qdH7tmpU3CXZzY2FqtsvM8ew9uN2WMA%3D%3D"
        url += "&cityCode="+ data['cityCode'] + "&routeId="+data['busRouteId'] + "&_type=json"
        req = requests.get(url=url)    
        temp = req.json()['response']['body']
        print(temp)
        if temp['totalCount'] >0:
            body = req.json()['response']['body']['items']['item']
            for ord in body :
                if ord['vehicleno'] == data['vehicleId']:
                    ordered = ord['nodeord']
                    print(ordered)
        else:
            return JsonResponse({'success': False, 'result': {}}, status=status.HTTP_404_NOT_FOUND)
        print(ordered)
        maxNode = 0
        queueList = list()
        if data['busRouteId'] is not None:
            flag = False
            queueFilter = QueueData.objects.filter(vehicleId = data['vehicleId'])
            if queueFilter is None : 
                return JsonResponse({'success' : False, 'result':{}}, status=status.HTTP_204_NO_CONTENT)
            else:
                if recentCheck :
                    recentCheck = False
                if data['busRouteId'] is not None:
                    route = routePerBus.objects.filter(busRouteId = data['busRouteId'])
                    for i in route:
                        if maxNode < i.nodeord:
                            maxNode = i.nodeord
                    print(maxNode)
                for i in range(0,4):
                    if maxNode < ordered + i:
                        print()
                    else:
                        print(i)
                        filterRouteList = route.filter(nodeord=ordered+i)[0].nodeId
                        print(filterRouteList)
                        stationsFilterList = busStationData.objects.filter(nodeId=filterRouteList)[0]
                        print(stationsFilterList.stationName)
                        queueList.append({'stationName':stationsFilterList.stationName, 'waiting' : False})
                for i in queueFilter:                        
                    queueOrder = i.stNodeOrder
                    if ordered <= queueOrder & queueOrder <= ordered +3:
                        if i.boardingCheck == 1 :
                            flag = True
                        queueList[queueOrder-ordered]['waiting'] = True
                if recentPostMan == recentMessageMan :
                    print("중복처리")
                else:
                    if recentVehicleId == data['vehicleId']:
                        recentData = busStationData.objects.filter(nodeId = recentNodeId)[0]
                        recentQueue = QueueData.objects.filter(uid = recentPostMan)[0]
                        tempIndex['recentResult']['stationName'] = recentData.stationName
                        tempIndex['recentResult']['queueTime'] = recentQueue.createAt
                        recentMessageMan = recentPostMan
                        return JsonResponse({'success':True, 'result':queueList,'boardingStatus' : flag,'message':tempIndex}, status=status.HTTP_200_OK)
                return JsonResponse({'success':True, 'result':queueList, 'boardingStatus' : flag, 'message':{}}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'success':False, 'result' : {}}, status = status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({'success':False, 'result':{}}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST']) 
def StationRouteInfo(request): # 사용자 어플 메인 데이터 API
    tempList = list()
    if request.method =='POST':        
        data = JSONParser().parse(request)
        userLocation = (data['gpsLati'], data['gpsLong'])
        stationsInfo = busStationData.objects.all() 
        for item in stationsInfo:
            temp = (item.latitude, item.longitude)
            distance = haversine(userLocation, temp) * 1000
            if distance < 700:
                stationsRouteInfo = routePerBus.objects.filter(nodeId = item.nodeId)
                stationsList = busStationData.objects.filter(nodeId= item.nodeId)
                routeInfo = list()
                for i in stationsRouteInfo:
                    temp = routeData.objects.filter(busRouteId=i.busRouteId)
                    routeInfo.append({
                        'description' : i.lfBus, #저상 버스
                        'name' : temp[0].routeNo +"-"+temp[0].destination+"방면", #방면
                        'id' : str(i.busRouteId),
                        'type' : "expand"
                    }) 
                tempList.append({'id': str(item.nodeId) ,'name':stationsList[0].stationName, 'description':str(int(distance))+"m",'type':"busStop" ,'routeData':routeInfo})
        print(len(tempList))
        if tempList[0]['id'] ==None :
            return JsonResponse({'success':False, 'result':{}}, status = status.HTTP_204_NO_CONTENT)
        return JsonResponse({'success' : True, 'result': tempList}, status=status.HTTP_200_OK)




@api_view(['POST'])
def searchKey(request): #사용자 어플에서 검색 API
    tempList = list()
    if request.method == 'POST':
        data = JSONParser().parse(request)
        tempslug = str(data['keyword'].replace(" ", ""))
        filterdItem = busStationData.objects.filter(stationName__icontains=tempslug)
        print(len(filterdItem))
        if len(filterdItem) == 0: #노선 정보일 때, 버스정류장이 아닐 때
            print("asd")
            filterdItem = routeData.objects.filter(routeNo__icontains=tempslug)
            if len(filterdItem) == 0:
                return JsonResponse({'success': False, 'result':{}}, status=status.HTTP_204_NO_CONTENT)
            for i in filterdItem:
                temps = routePerBus.objects.filter(busRouteId = i.busRouteId)
                tempList.append({'description': temps[0].lfBus, 'name' : i.routeNo + "-"+i.destination+"방면", 'id' : str(i.busRouteId), 'type':"bus", 'routeData':None})
            return JsonResponse({'success' : True, 'result': tempList}, status=status.HTTP_200_OK)
        else: #버스정류장 일때,
            routeFilter = routeData.objects.filter(routeNo__icontains=tempslug)
            if len(routeFilter) == 0: #버스정류장 정보만 존재할 때
                for i in filterdItem :
                    routeList = list()
                    tempGoe = (i.latitude, i.longitude)
                    userlocation = (data['gpsLati'], data['gpsLong'])
                    distance = haversine(tempGoe, userlocation) * 1000
                    routeFilter = routePerBus.objects.filter(nodeId= i.nodeId)
                    for item in routeFilter:
                        temp = routeData.objects.filter(busRouteId=item.busRouteId)
                        routeList.append({
                            'description' : item.lfBus,
                            'name': temp[0].routeNo + "-"+temp[0].destination+"방면",
                            'id':str(item.busRouteId),
                            'type':"expand"
                        })
                    
                    tempList.append({'id':i.nodeId, 'name':i.stationName, 'description' : str(int(distance))+"m"  ,'type':"busStop", 'routeData':routeList})
                return JsonResponse({'success':True, 'result':tempList}, status = status.HTTP_200_OK)
            else:
                filterdItem = busStationData.objects.filter(stationName__icontains=tempslug)
                
                for i in filterdItem :
                    routeList = list()
                    tempGoe = (i.latitude, i.longitude)
                    userlocation = (data['gpsLati'], data['gpsLong'])
                    distance = haversine(tempGoe, userlocation) * 1000
                    routeFilter = routePerBus.objects.filter(nodeId= i.nodeId)
                    for item in routeFilter:
                        temp = routeData.objects.filter(busRouteId=item.busRouteId)
                        routeList.append({
                            'description' : item.lfBus,
                            'name': temp[0].routeNo + "-"+temp[0].destination+"방면",
                            'id':str(item.busRouteId),
                            'type':"expand"
                        })
                    
                    tempList.append({'id':i.nodeId, 'name':i.stationName, 'description' : str(int(distance))+"m"  ,'type':"busStop", 'routeData':routeList})

                filterdItem = routeData.objects.filter(routeNo__icontains=tempslug)
                for i in filterdItem:
                    temps = routePerBus.objects.filter(busRouteId=i.busRouteId)
                    tempList.append({'description': temps[0].lfBus, 'name' : i.routeNo + "-"+i.destination+"방면",  'id' : str(i.busRouteId), 'type':"bus", 'routeData':None})

                return JsonResponse({'success':True, 'result':tempList}, status = status.HTTP_200_OK)

#POST CHECKING

def check_QueuePosting(nodeid, vehicleid, uid): #사용자가 Queue에 데이터를 등록할 때 flag를 날려주는 함수
    global postFlag, recentNodeId, recentVehicleId, recentPostMan
    postFlag = True
    recentNodeId = nodeid
    recentVehicleId = vehicleid
    recentPostMan = uid
    print("queue on data" + "nodeId = " + recentNodeId + "vehicleId = "+ recentVehicleId )

#----------------------------------------------------------------------------------------------------------------------------------------------
    #json을 읽어서 routeData와 busStationData를 DB에 저장하는 함수
def read_insert():
    json_routeInfo = dict()
    json_stationsInfo=dict()
    with open("routeInfo.json","r") as rt_json:
        json_routeInfo = json.load(rt_json)
    print(json_routeInfo)
    with open("stationsInfo.json", "r") as st_json:
        json_stationsInfo = json.load(st_json)
        
    for i in json_stationsInfo : 
        data = {'nodeId': i['nodeid'], 'latitude':i['gpslati'], 'longitude':i['gpslong'], 'stationName':i['nodenm'], 'cityCode' : "38030"}
        serializer = busSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
    for i in json_routeInfo :
        data = {'busRouteId' :"JJB"+i['노선아이디(ID)'], 'destination':i['방면'], 'routeNo':i['노선번호']}
        serializer = routeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()


  #json읽어서 해당 routeId가 경유하는 모든 정류장을 DB에 넣는 함수
def api_insert():
    json_routeInfo = dict()
    with open("routeInfo.json","r") as rt_json:
        json_routeInfo = json.load(rt_json)
    url = "http://openapi.tago.go.kr/openapi/service/BusRouteInfoInqireService/getRouteAcctoThrghSttnList?serviceKey=TGl%2FEQu3DnkXz1pe5Wyi3AveK9xofqEHe6zRAzkSH1DQ2eGsyOgiCp8qdH7tmpU3CXZzY2FqtsvM8ew9uN2WMA%3D%3D&_type=json"
    url += "&cityCode=38030&numOfRows=1000&routeId=JJB"

    for i in json_routeInfo:
        tempUrl = url+i['노선아이디(ID)']
        req = requests.get(tempUrl)
        body = req.json()['response']['body']['items']['item']
        for k in body:
            data = {'nodeId':k['nodeid'],'busRouteId':"JJB"+i['노선아이디(ID)'],'lfBus':"일반",'nodeord':k['nodeord']}
            serializer = routeBusStationSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            else:
                print(serializer.errors)


# API 호출해서 DB에 넣는 함수 
'''
def insert_nextStation():
    cityCode = ["38010","38030","38050","38070","38080","38090","38100","38310","38320","38330","38340","38350","38360","38370","38380","38390","38400"]
    for code in cityCode:
        call_getSttnNoList(cityCode=code)


def call_getSttnNoList(cityCode):
    url = "http://openapi.tago.go.kr/openapi/service/BusSttnInfoInqireService/getSttnNoList?serviceKey=TGl%2FEQu3DnkXz1pe5Wyi3AveK9xofqEHe6zRAzkSH1DQ2eGsyOgiCp8qdH7tmpU3CXZzY2FqtsvM8ew9uN2WMA%3D%3D&_type=json"
    url += "&numOfRows=999&cityCode="+cityCode
    req = requests.get(url)
    res = req.json()
    items = res['response']['body']['items']['item']

    for i in items:
        call_getSttnAcctoArvlPrearngeInfoList(cityCode=cityCode, nodeId=i['nodeid'] )


def call_getSttnAcctoArvlPrearngeInfoList(nodeId, cityCode):
    url = "http://openapi.tago.go.kr/openapi/service/ArvlInfoInqireService/getSttnAcctoArvlPrearngeInfoList?serviceKey=TGl%2FEQu3DnkXz1pe5Wyi3AveK9xofqEHe6zRAzkSH1DQ2eGsyOgiCp8qdH7tmpU3CXZzY2FqtsvM8ew9uN2WMA%3D%3D&_type=json"
    url += "&cityCode="+cityCode +"&nodeId="+nodeId
    req = requests.get(url)
    res = req.json()
    item = res['response']['body']['items']['item'][0]['routeid']

    print(res)
    call_getRouteAcctoThrghSttnList(nodeId=nodeId, routeId=item, cityCode=cityCode)


def call_getRouteAcctoThrghSttnList(nodeId, routeId, cityCode):
    url = "http://openapi.tago.go.kr/openapi/service/BusRouteInfoInqireService/getRouteAcctoThrghSttnList?serviceKey=TGl%2FEQu3DnkXz1pe5Wyi3AveK9xofqEHe6zRAzkSH1DQ2eGsyOgiCp8qdH7tmpU3CXZzY2FqtsvM8ew9uN2WMA%3D%3D&_type=json"
    url += "&cityCode="+cityCode+"&routeId="+routeId+"&numOfRows=1000&pageNo=1"
    req = requests.get(url)
    res = req.json()
    item = res['response']['body']['items']['item']
    filteredItem = ""
    for i in range(len(item)):
        if item[i]['nodeid'] == nodeId :
            filteredItem = item[i+1]['nodenm']
    print(filteredItem)
    insert_API_DATA(nodeid=nodeId, cityCode=cityCode, nextStation=filteredItem)        
    

def insert_API_DATA(cityCode, nodeid, nextStation):
    dataa = {'cityCode' : cityCode, 'nodeid' : nodeid, 'nextStation': nextStation}

    serializers = nodeSerializer(data=dataa)
    if serializers.is_valid():
        serializers.save()
    else:
        print(serializers.errors)


'''
