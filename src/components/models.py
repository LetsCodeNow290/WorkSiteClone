from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse
from checks.models import DailyCheck
from django.db.models import Max



# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f"{self.user} Profile"

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class MedicUnit(models.Model):
    unit_name = models.CharField(max_length=50, default='')
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.unit_name

    # def get_absolute_url(self):
    #     return reverse('medic_unit_update', kwargs={'pk': self.pk})


class Drug(models.Model):
    name = models.CharField(max_length=40)
    image = models.ImageField(default='default_drug.png', upload_to='drug_pics')
    is_active_safe = models.BooleanField(default=True)
    is_active_unit = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Vehicle(models.Model):
    property_number = models.IntegerField()
    unit_number = models.ForeignKey('MedicUnit', on_delete=models.PROTECT)
    image = models.ImageField(default='default_vehicle.jpg', upload_to='vehicle_profile_pics')
    make = models.CharField(max_length=40)
    model = models.CharField(max_length=40)
    year = models.IntegerField(default='2000')
    date_created = models.DateField(auto_now=True)
    mileage = models.IntegerField(default='0')
 
    def __str__(self):
        return str(self.property_number)
    
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def get_mileage(self):
        mileage_dict = {}
        for prop_num in self.objects.all():
            find_record = DailyCheck.objects.filter(unit_property_number=prop_num).latest('record_date')
            if find_record != None:
                mileage_dict.update({prop_num.property_number:find_record.mileage})
            else:
                continue
        return mileage_dict

    def get_location(self):
        location_dict = {}
        for prop_num in self.objects.all():
            find_record = DailyCheck.objects.filter(unit_property_number=prop_num).aggregate(Max('mileage'))
            if find_record['mileage__max'] != None:
                location_dict.update({prop_num.property_number:find_record['mileage__max']})
            else:
                continue
        return location_dict