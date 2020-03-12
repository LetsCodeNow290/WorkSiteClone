from django.contrib import admin
from .models import DailyCheck, NarcBox, RSIBag, WeeklyCheck

# Register your models here.
admin.site.register(DailyCheck)
admin.site.register(NarcBox)
admin.site.register(RSIBag)
admin.site.register(WeeklyCheck)