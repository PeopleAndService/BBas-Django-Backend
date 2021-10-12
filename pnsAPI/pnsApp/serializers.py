from django.db.models import fields
from rest_framework import serializers
from .models import QueueData, DriverAccount, PassengerAccount, RatingData, routeData, busStationData, routePerBus
class QueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueueData
        fields = ['uid', 'stbusStopId', 'edbusStopId', 'vehicleId', 'boardingCheck','busRouteId','stNodeOrder','edNodeOrder'] #JSON INPUT 목록
    
class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassengerAccount
        fields = ['uid', 'name', 'pushToken', 'pushSetting', 'emergencyPhone', 'cityCode', 'lfBusOption']

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverAccount
        fields = ['did', 'name', 'pushToken', 'pushSetting', 'verified', 'vehicleId', 'busRouteId']

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatingData
        fields = ['id', 'did', 'ratingData']

class busSerializer(serializers.ModelSerializer):
    class Meta:
        model = busStationData
        fields =['nodeId', 'latitude', 'longitude', 'stationName', 'cityCode']

class routeSerializer(serializers.ModelSerializer):
    class Meta:
        model = routeData
        fields =['busRouteId','destination','routeNo']

class routeBusStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = routePerBus
        fields =['nodeId','busRouteId','lfBus','nodeord']


'''

class QueueData(models.Model):  #신청 테이블
    id                      = models.BigAutoField(primary_key=True)
    uid                     = models.ForeignKey("PassengerAccount", related_name="user_data", on_delete=models.CASCADE, db_column="uid")
    stbusStopId             = models.CharField(max_length=50, null=False)
    edbusStopId             = models.CharField(max_length=50, null=False)
    vehicleId               = models.CharField(max_length=50, null=False)
    boardingCheck           = models.BooleanField(default=False, null=False)

class PassengerAccount(models.Model): #사용자 테이블
    uid                     = models.CharField(max_length=255, primary_key=True, null=False)
    email                   = models.CharField(max_length=45, null=False)       #user_id
    name                    = models.CharField(max_length=10, null=False)
    pushToken               = models.CharField(max_length=255, null=True)       #로그인 후에 푸쉬 세팅을 Allow 하면 토큰을 받아오고 로그아웃하거나, 푸쉬세팅을 not Allow하면 토큰을 지운다.
    pushSetting             = models.BooleanField(null=False, default=True)
    emergencyPhone          = models.CharField(max_length=13, null=True)
    verified                = models.BooleanField(null=False, default=False) 
    cityCode                = models.IntegerField(null=True, max_length=20)
    lfBusOption             = models.BooleanField(null=True, default=False)

class DriverAccount(models.Model): #사용자 테이블
    uid                     = models.CharField(max_length=255, primary_key=True, null=False)
    did                     = models.CharField(max_length=255, null=False)      #driver id
    email                   = models.CharField(max_length=45, null=False)       #user id
    name                    = models.CharField(max_length=10, null=False)
    pushToken               = models.CharField(max_length=255, null=True)       #로그인 후에 푸쉬 세팅을 Allow 하면 토큰을 받아오고 로그아웃하거나, 푸쉬세팅을 not Allow하면 토큰을 지운다.
    pushSetteing            = models.BooleanField(null=False, default=True)
    verified                = models.BooleanField(null=False, default=False)
    vehicleId               = models.CharField(max_length=50, null=False)
    busRouteId              = models.CharField(max_length=20, null=False)

class RatingData(models.Model):
    id                      = models.BigAutoField(primary_key=True)
    did                     = models.ForeignKey("DriverAccount", related_name="rated", on_delete=models.CASCADE, db_column="did")
    ratingData              = models.FloatField(max_length=5, null=False)

        '''