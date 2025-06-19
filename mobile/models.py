from django.db import models
from decimal import Decimal
from django.utils import timezone
# Create your models here.
class MobileDevice(models.Model):
    id = models.CharField(max_length=10,unique=True,db_index=True)
    name = models.CharField(max_length=10)
    at = models.DateTimeField(default=timezone.now)

class Data(models.Model):
    mobile_id = models.ForeignKey(MobileDevice,related_name="mobileId_data",db_index=True)
    lat = models.DecimalField()
    long = models.DecimalField()
    time = models.DateTimeField(db_index=True)
    cell_tech = models.CharField(db_index=True) #LTE ، HSPA+ ،HSPA،UMTS،EDGE ،GPRS, GSM، LTE-Adv, 5G
    cell_id = models.CharField(db_index=True)
    tac = models.CharField(db_index=True)
    rac_lac = models.CharField(db_index=True)
    PLMN_id = models.CharField(db_index=True)
    frequency = models.CharField(db_index=True)
    ARFCN = models.CharField(db_index=True) # and the real value
    power = models.DecimalField()
    quality = models.DecimalField() 
    quality_type = models.CharField() #RSRP, RSRQ, RSCP, Ec/N0, RxLev
    http_up = models.IntegerField()
    throughput_down = models.IntegerField()    
    throughput_UP = models.IntegerField()    
    ping = models.IntegerField()
    dns_t = models.IntegerField()
    web_t = models.IntegerField()
    sms_t = models.IntegerField()
