from django.db import models
from datetime import datetime # might not need

# Create your models here.

class Building(models.Model):
    
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, null= False)


class MeterData(models.Model):
   
    unit_choices = (('m3', 'm3'),('kWh','kWh'))

    class Fuel(models.TextChoices):
        water = 'w', 'water'
        fuel = 'f', 'fuel'
        electricity = 'e' ,'electricity'


    id = models.IntegerField(primary_key=True)
    building_id = models.ForeignKey(Building, to_field='id', on_delete=models.PROTECT)  # sets the foreign key to be the id in building
    fuel = models.CharField(max_length = 13, choices=Fuel.choices)
    unit = models.CharField(max_length = 4, choices=unit_choices)


class HalfhourlyData(models.Model):
    consumption = models.DecimalField(max_digits=9 ,decimal_places=5)
    meter_id = models.ForeignKey(MeterData, to_field='id', on_delete=models.PROTECT)
    reading_date_time = models.DateTimeField()
    