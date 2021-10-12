from datetime import time
from django.db import models
from django.db.models.deletion import DO_NOTHING
from django.db.models.fields import CharField, FloatField, IntegerField
from django.db.models.fields.related import ForeignKey

import time

class PassengerAccount(models.Model): #사용자 테이블
    uid                     = models.CharField(max_length=255, primary_key=True, null=False)
    name                    = models.CharField(max_length=10, null=False)
    pushToken               = models.CharField(max_length=255, null=True)       #로그인 후에 푸쉬 세팅을 Allow 하면 토큰을 받아오고 로그아웃하거나, 푸쉬세팅을 not Allow하면 토큰을 지운다.
    pushSetting             = models.BooleanField(null=False, default=False)
    emergencyPhone          = models.CharField(max_length=13, null=True)
    cityCode                = models.CharField(null=True, max_length=20)
    lfBusOption             = models.BooleanField(null=False, default=False)

    def __str__(self):
        return self.pushToken

class DriverAccount(models.Model): #사용자 테이블
    did                     = models.CharField(primary_key=True ,max_length=255, null=False)      #driver id
    name                    = models.CharField(max_length=10, null=False)
    pushToken               = models.CharField(max_length=255, null=True)       #로그인 후에 푸쉬 세팅을 Allow 하면 토큰을 받아오고 로그아웃하거나, 푸쉬세팅을 not Allow하면 토큰을 지운다.
    pushSetting             = models.BooleanField(null=False, default=False)
    verified                = models.BooleanField(null=False, default=False)
    vehicleId               = models.CharField(max_length=50, null=True)
    busRouteId              = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.pushToken

class QueueData(models.Model):  #신청 테이블x
    '''DB column'''
    uid                     = models.OneToOneField(PassengerAccount, on_delete=models.CASCADE, db_column="uid", primary_key=True)
    stbusStopId             = models.CharField(max_length=50, null=False)
    edbusStopId             = models.CharField(max_length=50, null=False)
    vehicleId               = models.CharField(max_length=50, null=False)
    busRouteId              = models.CharField(max_length=20, null=False)
    boardingCheck           = models.IntegerField(default=0, null=False)
    stNodeOrder             = models.IntegerField(null=False, default=0)
    edNodeOrder             = models.IntegerField(null=False, default=0)
    createAt                = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.boardingCheck

class RatingData(models.Model):
    id                      = models.AutoField(primary_key=True)
    did                     = models.ForeignKey(DriverAccount, related_name="rated", on_delete=models.CASCADE, db_column="did")
    ratingData              = models.FloatField(max_length=5, null=False)

    def __str__(self):
        return self.did

class busStationData(models.Model):
    nodeId                  = models.CharField(max_length=20, primary_key=True)
    latitude                = models.FloatField(null=False)
    longitude               = models.FloatField(null=False)
    stationName             = models.CharField(max_length=30, null=False)
    cityCode                = models.CharField(null=False, max_length=5)
    
    def __str__(self):
        return self.nodeId

class routeData(models.Model):
    busRouteId              = models.CharField(max_length=20, primary_key=True)
    destination             = models.CharField(max_length=30, null=False)
    routeNo                 = models.CharField(max_length=20, null=False)
    def __str__(self):
        return self.busRouteId

class routePerBus(models.Model):
    id                      = models.AutoField(primary_key=True)
    nodeId                  = models.ForeignKey(busStationData, on_delete=DO_NOTHING, db_column="nodeId")
    busRouteId              = models.ForeignKey(routeData, on_delete=DO_NOTHING, db_column="busRouteId")
    lfBus                   = models.CharField(max_length=20, null=False)
    nodeord                 = models.IntegerField(null=False, default=0)

    def __str__(self):
        return self.nodeId + self.busRouteId