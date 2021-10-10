from django import forms
from .models import Building, MeterData, HalfhourlyData


class BuildingForm(forms.ModelForm):
    
    class Meta:
        model = Building
        fields = ('id', 'name')

class MeterDataForm(forms.ModelForm):

    class Meta:
        model = MeterData
        fields = ('building_id', 'id', 'fuel', 'unit')


# couldn't get this to work. unit value wasn't available. is this because its fuel is processed before unit, so unit is not ready at that point?
    # def clean_fuel(self, *args, **kwargs):
    #     print("\n\nCLEANING FUEL")
    #     # ensure fuel matches the unit
    #     print("cleaned data is")
    #     print(self.cleaned_data)
    #     fuel = self.cleaned_data.get("fuel")
    #     unit = self.cleaned_data.get("unit")
    #     try:
    #         if fuel == 'water':
    #             assert unit == 'm3'
    #         elif fuel in ['Natural Gas', 'Electricity']:
    #             print("was in second one")
    #             assert unit == 'kWh'
    #         else:
    #             # fuel is none of the available options
    #             raise forms.ValidationError("Fuel field was empty")
    #         return fuel
    #     except:
    #         print("should be a validation error here")
    #         raise forms.ValidationError('Missmatch on fuel and unit given, or fuel not in available choices')


class HalfhourlyDataForm(forms.ModelForm):
       class Meta:
        model = HalfhourlyData
        fields = ('consumption', 'meter_id', 'reading_date_time')
