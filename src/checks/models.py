from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class DailyCheck(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    record_date = models.DateTimeField(auto_now=True)
    medic_unit_number = models.ForeignKey('components.MedicUnit', related_name='medic_unit_number', on_delete=models.PROTECT)
    emergency_lights = models.BooleanField()
    driving_lights = models.BooleanField()
    red_bag = models.BooleanField()
    LP_15 = models.BooleanField()
    BLS_bag = models.BooleanField()
    RTF_bag = models.BooleanField()
    Suction = models.BooleanField()
    oxygen = models.BooleanField()

class RSIBag(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    record_date = models.DateTimeField(auto_now=True)
    seal_number = models.IntegerField()
    incident_number = models.CharField(max_length=20)
    hospital = models.CharField(max_length=50)
    contact_EMS_Chief_date_and_time = models.CharField(max_length=50)

class NarcBox(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    record_date = models.DateTimeField(auto_now=True)
    seal_number = models.IntegerField()
    incident_number = models.CharField(max_length=20)
    hospital = models.CharField(max_length=50) 

    # Not yet migrated
    