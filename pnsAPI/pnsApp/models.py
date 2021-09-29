from django.db import models
class QueueData(models.Model):  #신청 테이블
    '''DB column'''
    busStopId               = models.CharField(max_length=50, null=False) #버스 정류장 ID
    busId                   = models.CharField(max_length=50, null=False) #버스 ID / 노선 ID 중에 하나가 될것 같음 
    userId                  = models.CharField(max_length=50, null=False) #사용자 ID forgein
    boardingCheck           = models.BooleanField(default=False, auto_created=True)
    
    def __str__(self):
        return self.busStopID

class PassengerAccount(models.Model): #사용자 테이블
    uid                     = models.CharField(max_length=255, primary_key=True, null=False)
    email                   = models.CharField(max_length=45, null=False)       #user_id
    name                    = models.CharField(max_length=10, null=False)
    pushToken               = models.CharField(max_length=255, null=True)       #로그인 후에 푸쉬 세팅을 Allow 하면 토큰을 받아오고 로그아웃하거나, 푸쉬세팅을 not Allow하면 토큰을 지운다.
    pushSetting             = models.BooleanField(null=False, default=True)
    emergencyPhone          = models.CharField(max_length=13, null=True)
    verified                = models.BooleanField(null=False, default=False)

    def __str__(self):
        return self.pushToken

class DriverAccount(models.Model): #사용자 테이블
    uid                     = models.CharField(max_length=255, primary_key=True, null=False)
    did                     = models.CharField(max_length=255, null=False)      #driver id
    email                   = models.CharField(max_length=45, null=False)       #user id
    name                    = models.CharField(max_length=10, null=False)
    pushToken               = models.CharField(max_length=255, null=True)       #로그인 후에 푸쉬 세팅을 Allow 하면 토큰을 받아오고 로그아웃하거나, 푸쉬세팅을 not Allow하면 토큰을 지운다.
    pushSetteing            = models.BooleanField(null=False, default=True)
    verified                = models.BooleanField(null=False, default=False)

    def __str__(self):
        return self.pushToken
