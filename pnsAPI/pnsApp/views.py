from django.shortcuts import render

from django.http.response import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status

from .models import daDB, Account
from .serializers import pnsAPIserializers, AccountSerializers
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

@api_view(['GET','POST', 'PUT', 'DELETE'])
def pns_list(request, pk):
    try:
        pnsdata = daDB.objects

    except daDB.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        if pk == "0":
            pnsdata = pnsdata.all()
            serializer = pnsAPIserializers(pnsdata, many=True)
            return JsonResponse(serializer.data, safe=False)
        else:
            pnsdata = pnsdata.get(id=pk)
            serializer = pnsAPIserializers(pnsdata)
            return JsonResponse(serializer.data)
            
    elif (request.method == 'POST'):
        pns_data = JSONParser().parse(request)
        pns_serializer = pnsAPIserializers(data = pns_data)
        if pns_serializer.is_valid():
            pns_serializer.save()
            return JsonResponse(pns_serializer.data, status = status.HTTP_201_CREATED)
        return JsonResponse(pns_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif (request.method == 'PUT'):
        data = JSONParser().parse(request)
        serializer = pnsAPIserializers(pnsdata, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif (request.method == 'DELETE'):
        pnsdata.delete()
        return JsonResponse(status=204)


