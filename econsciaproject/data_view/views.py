from django.shortcuts import render
from upload_csv.models import Building, MeterData, HalfhourlyData
from django.http.response import HttpResponse


# Create your views here.

        # get all data for each Building
        #
        # Building                  Meter
        # ------------------------------------------
        #  Aberdeen                 Electric
        #                           Water
        # ------------------------------------------
        #  Bristol                   Fuel
        # ------------------------------------------
        # 
        #

def present_all_data(request):
    context = {}
    building_set = set()
    meter_dict = {}

    if request.method =='GET':

        all_buildings = Building.objects.all().order_by('name') 
        for building in all_buildings:

            # get all meters related to the building
            meters = MeterData.objects.filter(building_id=building.building_id)
            meter_ids = []
            for meter in meters:
                meter_ids.append(meter.meter_id)
            meter_dict[building] = meter_ids


        context['meter_dict'] = meter_dict


        return render(request, "data_view/showdata.html", context)


def specific_meter(request):
    if request.method == 'GET':
        context = {}
        meter_id = request.GET.get('meter_id','')
        try:
            # cast to int, so it catches if someones input a non-number string
            meter_id = int(meter_id)
            meter = MeterData.objects.get(meter_id=meter_id)
        except:
            return HttpResponse("General error originating from building_id")

        consumption_data = HalfhourlyData.objects.filter(meter=meter_id)
        context['meter'] = meter
        context['consumption_data'] = consumption_data
    return render(request, "data_view/meter_view.html", context)


def specific_building(request):

    if request.method == 'GET':

        building_id = request.GET.get('building_id','')

        try:
            building_id = int(building_id)
            meters = MeterData.objects.filter(building_id=building_id)
            building_name = Building.objects.get(building_id=building_id).name

        except Exception as e:
            print(e)
            return HttpResponse("General error originating from building_id")

        half_hourly_dict = {}
        context = {}
        date_range = set()

        # Each building can have multiple meters. so for each metet we need to get the meter readings
        for meter_id in meters:
            half_hourly_dict[meter_id] = HalfhourlyData.objects.filter(meter=meter_id).order_by('reading_date_time')

            # get a set of times to label the line graph
            times = HalfhourlyData.objects.values_list('reading_date_time').filter( meter=meter_id)
            date_range.update(times)

        # convert datetimes into a nice string for the line graph
        new_date_range = []
        for i in date_range:
            new_date_range.append(i[0].strftime("%m/%d/%Y, %H:%M:%S"))
        
        # add all data to the context
        context['date_range'] = new_date_range
        context['meter_dict'] = half_hourly_dict
        context['building_name'] = building_name

        return render(request, "data_view/building_view.html", context)