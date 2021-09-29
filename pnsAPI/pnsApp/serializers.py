from rest_framework import serializers
from .models import QueueData, DriverAccount, PassengerAccount

class pnsAPIserializer(serializers.ModelSerializer):
    class Meta:
        model = QueueData
        fields = ['busStopId', 'busId', 'userId', 'boardingCheck'] #JSON INPUT 목록
    

class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassengerAccount
        fields = ['uid', 'email', 'name', 'pushToken', 'pushSetting', 'emergencyPhone', 'verified']

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverAccount
        fields = ['uid', 'did', 'email', 'name', 'pushToken', 'pushSetting', 'verified']


        '''
        QUEUEDATA
    busStopId               = models.CharField(max_length=50, null=False)
    busId                   = models.CharField(max_length=50, null=False)
    userId                  = models.CharField(max_length=50, null=False)
    boardingCheck           = models.BooleanField(default=False, auto_created=True)
        PASSENGERACCOUNT
    uid                     = models.CharField(max_length=255, primary_key=True, null=False)
    email                   = models.CharField(max_length=45, null=False)       
    name                    = models.CharField(max_length=10, null=False)
    pushToken               = models.CharField(max_length=255, null=True)       
    pushSetting             = models.BooleanField(null=False, default=True)
    emergencyPhone          = models.CharField(max_length=13, null=True)
    verified                = models.BooleanField(null=False, default=False)
        DRIVERACCOUNT
    uid                     = models.CharField(max_length=255, primary_key=True, null=False)
    did                     = models.CharField(max_length=255, null=False)      
    email                   = models.CharField(max_length=45, null=False)       
    name                    = models.CharField(max_length=10, null=False)
    pushToken               = models.CharField(max_length=255, null=True)       
    pushSetteing            = models.BooleanField(null=False, default=True)
    verified                = models.BooleanField(null=False, default=False)
        '''