from django.db import models
from datetime import datetime # might not need
from django import forms


# Create your models here.

class Building(models.Model):
    
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, null= False)

    def __str__(self) -> str:
        return self.name

class MeterData(models.Model):
   
    unit_choices = (('m3', 'm3'),('kWh','kWh'))

    class Fuel(models.TextChoices):
        water = 'Water', 'Water'
        natural_gas = 'Nautral Gas', 'Natural Gas'
        electricity = 'Electricity' ,'Electricity'

    # building_id = models.IntegerField()
    building_id = models.ForeignKey(Building, to_field='id', on_delete=models.CASCADE)  # sets the foreign key to be the id in building
    meter_id = models.IntegerField(null=True) # not used as primary key as buildings can have more than 1 meter
    fuel = models.CharField(max_length = 13)#, choices=Fuel.choices)
    unit = models.CharField(max_length = 10)# , choices=unit_choices)


    def __str__(self) -> str:
        return str(self.id)


class HalfhourlyData(models.Model):
    consumption = models.DecimalField(max_digits=9 ,decimal_places=5)
    # meter_id = models.ForeignKey(MeterData, to_field='id', on_delete=models.CASCADE)
    meter_id = models.IntegerField()
    reading_date_time = models.DateTimeField()
    