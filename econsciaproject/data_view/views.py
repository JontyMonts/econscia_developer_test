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
        if not meter_id:
            return HttpResponse("There was no meter id parsed")
        try:
            meter = MeterData.objects.get(meter_id=meter_id)
        except MeterData.DoesNotExist:
            return HttpResponse("Error when finding meter")

        consumption_data = HalfhourlyData.objects.filter(meter=meter_id)
        context['meter'] = meter
        context['consumption_data'] = consumption_data
    return render(request, "data_view/meter_view.html", context)


def specific_building(request):

    if request.method == 'GET':

        building_id = request.GET.get('building_id','')
        building_name = Building.objects.get(building_id=building_id).name
        print(building_name)
        # if no id set, or if id was incorrect (no such id or str instead of int)
        if not building_id:
            return HttpResponse("There was no building id parsed")

        try:
            meters = MeterData.objects.filter(building_id=building_id)
        except MeterData.DoesNotExist:
            return HttpResponse("No meters were found for that building id")



        half_hourly_dict = {}
        context = {}
        date_range = set()
        for meter_id in meters:
            half_hourly_dict[meter_id] = HalfhourlyData.objects.filter(meter=meter_id).order_by('reading_date_time')

            # get a set of times to label the line graph
            times = HalfhourlyData.objects.values_list('reading_date_time').filter( meter=meter_id)
            date_range.update(times)

        # sort times into ascending order
        print(sorted(date_range))
        print(date_range)
        new_date_range = []
        print()
        for i in date_range:
            new_date_range.append(i[0].strftime("%m/%d/%Y, %H:%M:%S"))
        
        context['date_range'] = new_date_range
        context['meter_dict'] = half_hourly_dict
        context['building_name'] = building_name

        # need to get range of half hourly datas which is 2018-12-01 at 00:00 to 2018-12-31 at 23:30

        html = "<html><body>It is now.</body></html>" 
        return render(request, "data_view/building_view.html", context)