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
            meter_dict[building.name] = meter_ids


        context['meter_dict'] = meter_dict


        return render(request, "data_view/showdata.html", context)


def specific_meter(request):
    pass

def specific_building(request):

    if request.method == 'GET':

        building_id = request.GET.get('building_id','')

        if not building_id:
            return HttpResponse("There was no building id parsed")
        
        half_hourly_dict = {}
        context = {}

        meters = MeterData.objects.filter(building_id=building_id)
        for meter_id in meters:
            half_hourly_dict[meter_id] = HalfhourlyData.objects.filter(meter=meter_id)

        context['meter_dict'] = half_hourly_dict
        html = "<html><body>It is now.</body></html>" 
        return render(request, "data_view/building_view.html", context)