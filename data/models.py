from django.db import models
from user.models import Device

class CellMeasurement(models.Model):
    # user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="cell_measurements")
    deviceId = models.ForeignKey(Device,null=True, blank=True, on_delete=models.SET_NULL)
    latitude = models.FloatField()
    longitude = models.FloatField()
    signal_level = models.IntegerField(null=True, blank=True)
    carrier = models.CharField(max_length=100, null=True, blank=True)
    technology = models.CharField(max_length=50, null=True, blank=True)
    tac = models.IntegerField(null=True, blank=True)
    plmn_id = models.CharField(max_length=20, null=True, blank=True)
    arfcn = models.IntegerField(null=True, blank=True)
    rsrq = models.IntegerField(null=True, blank=True)
    rsrp = models.IntegerField(null=True, blank=True)
    rscp = models.IntegerField(null=True, blank=True)
    ec_no = models.IntegerField(null=True, blank=True)
    rx_lev = models.IntegerField(null=True, blank=True)
    time = models.DateTimeField()
    # created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-time']

    def __str__(self):
        return f"{self.carrier} - {self.technology}"


class TestResult(models.Model):
    deviceId = models.ForeignKey(Device,null=True, blank=True,on_delete=models.SET_NULL)
    latitude = models.FloatField()
    longitude = models.FloatField()
    throughput = models.BigIntegerField(null=True, blank=True)  # KB/s
    ping = models.BigIntegerField(null=True, blank=True)       # ms
    web = models.BigIntegerField(null=True, blank=True)        # ms
    dns = models.BigIntegerField(null=True, blank=True)        # ms
    sms = models.BigIntegerField(null=True, blank=True)        # ms
    time = models.DateTimeField()
    # created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-time']

    def __str__(self):
        return f"TestResult {self.id}"
