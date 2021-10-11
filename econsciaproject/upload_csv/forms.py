from django import forms
from .models import Building, MeterData, HalfhourlyData


class BuildingForm(forms.ModelForm):
    
    class Meta:
        model = Building
        fields = ('building_id', 'name')

class MeterDataForm(forms.ModelForm):

    class Meta:
        model = MeterData
        fields = ('building', 'meter_id', 'fuel', 'unit')


class HalfhourlyDataForm(forms.ModelForm):
       class Meta:
        model = HalfhourlyData
        fields = ('consumption', 'meter', 'reading_date_time')
