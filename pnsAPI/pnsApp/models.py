from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
class daDB(models.Model):  #신청 테이블
    '''DB column'''
    busStopId               = models.CharField(max_length=50, null=False) #버스 정류장 ID
    busId                   = models.CharField(max_length=50, null=False) #버스 ID / 노선 ID 중에 하나가 될것 같음 
    userId                  = models.CharField(max_length=50, null=False) #사용자 ID forgein
    boardingCheck           = models.BooleanField(default=False, auto_created=True)
    
    def __str__(self):
        return self.busStopID

class Account(models.Model): #사용자 테이블
    userId                  =models.CharField(max_length=50, primary_key=True)
    userName                =models.CharField(max_length=15, null=True)
    password                =models.CharField(max_length=400)
    email                   =models.EmailField(max_length=200)
    token                   =models.CharField(max_length=200)
    is_activate             =models.BooleanField(default=False)
    created_at              =models.DateTimeField(auto_now_add=True)
    updated_at              =models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering =['created_at']