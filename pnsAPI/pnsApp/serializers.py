from rest_framework import serializers
from .models import daDB, Account

class pnsAPIserializers(serializers.ModelSerializer):
    class Meta:
        model = daDB
        fields = ['id','busStopId', 'busId', 'userId','boardingCheck'] #JSON INPUT 목록
    

class AccountSerializers(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['userId','userName','password', 'token', 'email']
