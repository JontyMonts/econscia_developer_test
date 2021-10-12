from django.db import models
from datetime import datetime # might not need
from django import forms


# Create your models here.

class Building(models.Model):
    
    building_id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=100, null= False)

    def __str__(self) -> str:
        return self.name

class MeterData(models.Model):

    building = models.ForeignKey(Building, to_field='building_id', on_delete=models.CASCADE)  # sets the foreign key to be the id in building
    meter_id = models.IntegerField(primary_key=True) # why does this have to be null = true?
    fuel = models.CharField(max_length = 13)
    unit = models.CharField(max_length = 10)


    def __str__(self) -> str:
        return str("{}-{}".format(self.meter_id,self.fuel))


class HalfhourlyData(models.Model):
    consumption = models.DecimalField(max_digits=9 ,decimal_places=5)
    meter = models.ForeignKey(MeterData, to_field='meter_id', on_delete=models.CASCADE) # this can't be foreign key as multiple meter datas to one building
    # meter_id = models.IntegerField()
    reading_date_time = models.DateTimeField()
    