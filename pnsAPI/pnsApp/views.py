from django.shortcuts import render

from django.http.response import HttpResponse, JsonResponse
from drf_yasg.openapi import Response
from rest_framework.parsers import JSONParser 
from rest_framework import status

from .models import QueueData, PassengerAccount, DriverAccount, RatingData
from .serializers import DriverSerializer, PassengerSerializer, QueueSerializer, RatingSerializer
from rest_framework.decorators import api_view
from rest_framework import generics

import hashlib


'''
---------------------DataBase management area--------------------------
if(request.method == 'GET'):  #request에서 받은 값으로 쿼리 하는 구문
        data = JSONParser().parse(request)
        if data['id'] is not None:
            pnsData = daDB.objects.filter(id=data['id'])
            serializedData = pnsAPIserializers(pnsData, many=True)
            return JsonResponse(serializedData.data, safe=False)
        elif data['busStopId'] is not None:
            pnsData = daDB.objects.filter(busStopId=data['busStopId'])
            serializedData = pnsAPIserializers(pnsData, many=True)
            return JsonResponse(serializedData.data, safe=False)
        elif data['busId'] is not None:
            pnsData = daDB.objects.filter(busId=data['busId'])
            serializedData = pnsAPIserializers(pnsData, many=True)
            return JsonResponse(serializedData.data, safe=False)
        elif data['userId'] is not None:
            pnsData = daDB.objects.filter(userId=data['userId'])
            serializedData = pnsAPIserializers(pnsData, many=True)
            return JsonResponse(serializedData.data, safe=False)
        elif data['boardingCheck'] is not None:
            pnsData = daDB.objects.filter(boardingCheck=data['boardingCheck'])
            serializedData = pnsAPIserializers(pnsData, many=True)
            return JsonResponse(serializedData.data, safe=False)
'''

@api_view(['GET', 'PUT', 'DELETE'])
def queuelist(request, pk):                     #QueueData API/CRUD
    try:
        qdata = QueueData.objects

    except QueueData.DoesNotExist:
        return JsonResponse({'success':False, 'result': None},status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        if pk == "0":
            qsdata = qdata.all()
            qserializer = QueueSerializer(qsdata, many=True)
            return JsonResponse(qserializer.data, safe=False)
        else:
            qsdata = qdata.get(id=pk)
            qserializer = QueueSerializer(qsdata)
            return JsonResponse(qserializer.data)


@api_view(['POST'])
def queue(request):         
    if (request.method == 'POST'):
        q_data = JSONParser().parse(request)
        q_serializer = QueueSerializer(data = q_data)
        if q_serializer.is_valid():
            q_serializer.save()
            return JsonResponse(q_serializer.data, status = status.HTTP_201_CREATED)
        return JsonResponse(q_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#------------------------------------------------------------------------------------------------------------


@api_view(['POST', 'PUT', 'DELETE'])
def passengerByUid(request):                     #passengerAccount by uid
    try:
        data = JSONParser().parse(request)
        passengerData = PassengerAccount.objects.filter(uid=data['uid'])
    except PassengerAccount.DoesNotExist:
        return JsonResponse({'success':False, 'result': None},status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        if data['uid'] is not None:
            if len(passengerData) == 0 :
                return JsonResponse({'success':False,'result': None}, safe=False, status = status.HTTP_204_NO_CONTENT)
            else:
                serializedData = PassengerSerializer(passengerData, many=True)
                return JsonResponse({'success':True,'result': serializedData.data[0]}, safe=False, status=status.HTTP_200_OK)
        else:
            return JsonResponse(status=400)
            
    elif (request.method == 'PUT'):
        if data['uid'] is not None:
            if len(passengerData) == 0 :
                return JsonResponse({'success':False,'result': None}, safe=False, status=status.HTTP_204_NO_CONTENT)
            else:
                passengerData = passengerData.get()
                serializer = PassengerSerializer(passengerData,data = data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse({'success':True,'result': serializer.data}, safe=False, status=status.HTTP_200_OK)
                else:
                    return JsonResponse({'success':False,'result': None}, safe=False, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({'success':False, 'result':None},status=status.HTTP_400_BAD_REQUEST)

    elif (request.method == 'DELETE'):
        if data['uid'] is not None:
            filteredData = passengerData.filter(uid=data['uid'])
            filteredData.delete()
            return JsonResponse({'success':True, 'result':None},status=status.HTTP_204_NO_CONTENT)
        else:
            return JsonResponse({'success':False, 'result':None},status=status.HTTP_400_BAD_REQUEST)

#------------------------------------------------------------------------------------------------------------

@api_view(['POST', 'PUT', 'DELETE'])
def driverByUid(request):                     #driverAccount by uid
    try:
        data = JSONParser().parse(request)
        driverData = DriverAccount.objects.filter(did=data['did'])
    except DriverAccount.DoesNotExist:
        return JsonResponse({'success':False, 'result': None},status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        if data['did'] is not None:
            if len(driverData) == 0:
                return JsonResponse({'success':False,'result': None}, safe=False, status=status.HTTP_204_NO_CONTENT)
            else:
                filteredData = driverData.filter(did=data['did'])
                serializedData = DriverSerializer(filteredData, many=True)
                return JsonResponse({'success':True,'result': serializedData.data[0]}, safe=False, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'success':False, 'result':None},status=status.HTTP_400_BAD_REQUEST)

    elif (request.method == 'PUT'):
        if data['did'] is not None:
            if len(driverData) == 0:
                return JsonResponse({'success':False,'result': None}, safe=False, status=status.HTTP_204_NO_CONTENT)
            else:
                driverData = driverData.get()
                d_serializer = DriverSerializer(driverData, data=data)
                if d_serializer.is_valid():
                    d_serializer.save()
                    return JsonResponse({'success':True,'result': d_serializer.data}, safe=False, status=status.HTTP_200_OK)
                else:
                    return JsonResponse({'success':False,'result': None}, safe=False, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({'success':False, 'result':None},status=status.HTTP_400_BAD_REQUEST)

    elif (request.method == 'DELETE'):
        if data['did'] is not None:
            filteredData = driverData.get()
            filteredData.delete()
            return JsonResponse({'success':True,'result': None},status=status.HTTP_204_NO_CONTENT)
        else:
            return JsonResponse({'success':False,'result': None},status=status.HTTP_400_BAD_REQUEST)


#------------------------------------------------------------------------------------------------------------

@api_view(['GET', 'PUT', 'DELETE'])
def ratinglist(request, pk):                     #rating API/CRUD
    try:
        rateData = RatingData.objects

    except RatingData.DoesNotExist:
        return JsonResponse({'success':False, 'result': None},status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        if pk == "0":
            rdata = rateData.all()
            ratingserializer = RatingSerializer(rdata, many=True)
            return JsonResponse(ratingserializer.data, safe=False)
        else:
            rdata = rateData.get(id=pk)
            ratingserializer = RatingSerializer(rdata)
            return JsonResponse(ratingserializer.data)



@api_view(['POST'])
def rating(request):
    if (request.method == 'POST'):
        r_data = JSONParser().parse(request)
        r_serializer = RatingSerializer(data = r_data)
        if r_serializer.is_valid():
            r_serializer.save()
            return JsonResponse(r_serializer.data, status = status.HTTP_201_CREATED)
        return JsonResponse(r_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#------------------------------------------------------------------------------------------------------------

@api_view(['POST'])
def passengerSign(request):
    try:
        passengerData = PassengerAccount.objects
        data = JSONParser().parse(request)
    except PassengerAccount.DoesNotExist:
        return JsonResponse({'success':False, 'result': None},status=status.HTTP_404_NOT_FOUND)
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
                return JsonResponse({"success" : False, "result": None}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return JsonResponse({"success" : False, "result": None}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({"success" : False, "result": None}, status=status.HTTP_403_FORBIDDEN)

@api_view(['POST'])
def driverSign(request):
    try:
        driverData = DriverAccount.objects
        data = JSONParser().parse(request)
    except DriverAccount.DoesNotExist:
        return JsonResponse({'success':False, 'result': None},status=status.HTTP_404_NOT_FOUND)
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
                return JsonResponse({"success" : False, "result": None}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return JsonResponse({"success" : False, "result": None}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({"success" : False, "result": None}, status=status.HTTP_403_FORBIDDEN)
    



'''
Driver - 출근, 퇴근 먼저하셈 업데이트
'''
