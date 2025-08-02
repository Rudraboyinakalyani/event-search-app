from django.db import models

# Create your models here.
class Event(models.Model):
    serialno = models.IntegerField()
    version = models.IntegerField(null=True, blank=True)
    account_id = models.CharField(max_length=100, null=True, blank=True)
    instance_id = models.CharField(max_length=100, null=True, blank=True)
    srcaddr = models.GenericIPAddressField()
    dstaddr = models.GenericIPAddressField()
    srcport = models.IntegerField(null=True, blank=True)
    dstport = models.IntegerField(null=True, blank=True)
    protocol = models.CharField(max_length=20, null=True, blank=True)
    packets = models.IntegerField(null=True, blank=True)
    bytes = models.BigIntegerField(null=True, blank=True)
    starttime = models.BigIntegerField()
    endtime = models.BigIntegerField()
    action = models.CharField(max_length=20, null=True, blank=True)
    log_status = models.CharField(max_length=20, null=True, blank=True)
    file_name = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return f"{self.srcaddr} --> {self.dstaddr} | Action: {self.action}"


