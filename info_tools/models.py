from django.db import models


# Create your models here.

class InternetUsageData(models.Model):
    username = models.CharField(blank=False, null=False, max_length=100)
    mac_address = models.CharField(blank=False, null=False, max_length=100)
    start_time = models.DateTimeField(blank=False, null=False)
    usage_time = models.TimeField(blank=False, null=False)
    upload = models.FloatField(blank=False, null=False)
    download = models.FloatField(blank=False, null=False)

    class Meta:
        db_table = "InternetUsageData"
        managed = True
