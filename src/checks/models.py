from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class DailyCheck(models.Model):
    daily_user = models.ForeignKey(User, on_delete=models.PROTECT)
    record_date = models.DateTimeField(auto_now=True)
    medic_unit_number = models.ForeignKey('components.MedicUnit', related_name='medic_unit_number', on_delete=models.PROTECT, default='')
    unit_property_number = models.ForeignKey('components.Vehicle', related_name='unit_property_number', on_delete=models.PROTECT, default='')
    mileage = models.IntegerField(default=0)
    emergency_lights = models.BooleanField()
    driving_lights = models.BooleanField()
    red_bag = models.BooleanField()
    LP_15 = models.BooleanField()
    BLS_bag = models.BooleanField()
    RTF_bag = models.BooleanField()
    suction = models.BooleanField()
    oxygen = models.BooleanField()
    free_text = models.TextField(default='')

    #Need to fix all the templates for the vehicles

class RSIBag(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    record_date = models.DateTimeField(auto_now=True)
    seal_number = models.IntegerField()
    incident_number = models.CharField(max_length=20)
    hospital = models.CharField(max_length=50)
    contact_EMS_Chief = models.CharField(max_length=100, default='')
    free_text = models.TextField(default='')

class NarcBox(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    record_date = models.DateTimeField(auto_now=True)
    seal_number = models.IntegerField()
    narc_name = models.ForeignKey('components.Drug', related_name='narc_name', on_delete=models.PROTECT, default=0, limit_choices_to={'is_active_unit': True})
    amount_removed_unit = models.IntegerField(blank=True, null=True, default=0)
    amount_added_unit = models.IntegerField(blank=True, null=True, default=0)
    amount_in_unit = models.IntegerField(blank=True, null=True, default=0)
    incident_number = models.CharField(max_length=20)
    hospital = models.CharField(max_length=50)
    narc_box_free_text = models.TextField(default='', blank=True)

    # Need to add this to urls.py
    