from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import datetime

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
    RSI_seal_number = models.IntegerField()
    next_expiration_date = models.DateField(default=datetime.now)
    incident_number = models.CharField(max_length=20, blank=True, null=True)
    hospital = models.CharField(max_length=50, blank=True, null=True)
    contact_EMS_Chief = models.DateTimeField(default=datetime.now, blank=True, null=True)
    free_text = models.TextField(default='')

class NarcBox(models.Model):
    narc_medic_unit_number = models.ForeignKey('components.MedicUnit', related_name='narc_medic_unit_number', on_delete=models.PROTECT, default='')
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    record_date = models.DateTimeField(auto_now=True)
    seal_number = models.IntegerField()
    narcotic_name = models.ForeignKey('components.Drug', related_name='narc_name', on_delete=models.PROTECT, default=0, limit_choices_to={'is_active_unit': True})
    amount_given_to_patient = models.IntegerField(blank=True, null=True, default=0)
    amount_removed_from_unit = models.IntegerField(blank=True, null=True, default=0)
    amount_added_to_unit = models.IntegerField(blank=True, null=True, default=0)
    amount_in_unit = models.IntegerField(blank=True, null=True, default=0)
    incident_number = models.CharField(max_length=20,blank=True, null=True)
    hospital = models.CharField(max_length=50, blank=True, null=True)
    narc_box_free_text = models.TextField(default='', blank=True)

FLUID_CHOICES = (
    ('Within Range', 'Within Range'),
    ('Needs More', 'Needs More')
)
TIRE_CHOICES = (
    ('Full','Full'),
    ('Low', 'Low'),
    ('Flat', 'Flat')
)

class WeeklyCheck(models.Model):
    weekly_unit_number = models.ForeignKey('components.MedicUnit', related_name='weekly_unit_number', on_delete=models.PROTECT, default='')
    weekly_user = models.ForeignKey(User, on_delete=models.PROTECT)
    weekly_record_date = models.DateTimeField(auto_now=True)
    engine_oil = models.CharField(max_length=20, choices=FLUID_CHOICES, default='Within Range')
    transmission_fluid = models.CharField(max_length=20, choices=FLUID_CHOICES, default='Within Range')
    brake_fluid = models.CharField(max_length=20, choices=FLUID_CHOICES, default='Within Range')
    coolant = models.CharField(max_length=20, choices=FLUID_CHOICES, default='Within Range')
    LUCAS_device = models.CharField(max_length=30, choices=(('Functional', 'Functional'), ('Needs Repair', 'Needs Repair')), default='Functional')
    EMS_equipment = models.CharField(max_length=50, choices=(('All equiment is present, functional and in date', 'All equiment is present, functional and in date'), ('Some euipment missing (See Comments)', 'Some euipment missing (See Comments)'), ('Items out of date (See Comments)', 'Items out of date (See Comments)')), default='All equiment is present, functional and in date')
    suciton_unit = models.CharField(max_length=30, choices=(('Charged', 'Charged'), ('On Charge', 'On Charge'), ('Not Charging', 'Not Charging')), default='Charged')
    driver_front_tire = models.CharField(max_length=30, choices=TIRE_CHOICES, default='Full')
    driver_rear_tire = models.CharField(max_length=30, choices=TIRE_CHOICES, default='Full')
    passenger_front_tire = models.CharField(max_length=30, choices=TIRE_CHOICES, default='Full')
    passenger_rear_tire = models.CharField(max_length=30, choices=TIRE_CHOICES, default='Full')
    comments = models.TextField(blank=True, null=True)

    # Need to add this to urls.py
    