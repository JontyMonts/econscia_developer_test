from django import forms
from .models import Building, MeterData, HalfhourlyData


class BuildingForm(forms.ModelForm):
    
    class Meta:
        model = Building
        fields = ('id', 'name')

class MeterDataForm(forms.ModelForm):

    class Meta:
        model = MeterData
        fields = ('id', 'building_id', 'fuel', 'unit')

class HalfhourlyDataForm(forms.ModelForm):
       class Meta:
        model = HalfhourlyData
        fields = ('consumption', 'meter_id', 'reading_date_time')
