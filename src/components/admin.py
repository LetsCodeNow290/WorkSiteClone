from django.contrib import admin
from .models import UserProfile,MedicUnit, Drug

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(MedicUnit)
admin.site.register(Drug)