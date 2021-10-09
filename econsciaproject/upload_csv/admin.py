from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Building, MeterData, HalfhourlyData

admin.site.register(Building)
admin.site.register(MeterData)
admin.site.register(HalfhourlyData)
