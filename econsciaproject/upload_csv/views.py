from django.http.response import HttpResponse
from django.shortcuts import render
import logging
from .models import Building, MeterData, HalfhourlyData
from.forms import BuildingForm, MeterDataForm, HalfhourlyDataForm

# Create your views here.
# logger = logging.getLogger(__name__)
# logger.debug("did this work?")


def upload_csv(request):
    if "GET" == request.method:
        return render(request, "upload_csv/upload_csv.html", {})


    elif "POST" == request.method:

        csv_file = request.FILES['csv_file']
        file_data = csv_file.read().decode('utf-8')
        lines = file_data.split("\r\n")
        msg = "Generic Error"
        all_errors = []
        
        # Handle the 3 different types of csv we will get

        if request.POST['csv_type'] == 'building':

            # check that the column names match to the building table
            if 'id,name' in lines[0]:     
                # we don't want the first line              
                for line in lines[1:]:
                    # split the data
                    fields = line.split(",")
                    # check that the line has data in it, as there are empty lines at the bottom of the file
                    if fields[0] != '':
                        data_dict = {}
                        data_dict["building_id"] = fields[0]
                        data_dict["name"] = fields[1]
                        # Save the row to the database 
                        try:
                            form = BuildingForm(data_dict)
                            if form.is_valid():
                                form.save()
                                msg = "successfully uploaded building data"
                            else:
                                msg = form.errors
                        except Exception as e:
                            msg = form.errors         
            else:
                msg = "this was not a building csv file"


        elif request.POST['csv_type'] == 'meter':
            # if headers matches meter upload file then do logic
            if 'building_id,id,fuel,unit' in lines[0]:
                for line in lines[1:-1]: # FIXME some reason the last line is entered twice
                    fields = line.split(",")
                    if fields[0] != '':
                        msg = "setting data dict"
                        data_dict = {}
                        data_dict["building"] = fields[0]
                        data_dict["meter_id"] = fields[1]
                        data_dict["fuel"] = fields[2]
                        data_dict["unit"] = fields[3]
                    try:
                        form = MeterDataForm(data_dict)
                        if form.is_valid():
                            form.save()
                            msg = "successfully uploaded meter data"
                        else:
                            msg = form.errors
                            all_errors.append(data_dict['meter_id'])

                    except Exception as e:
                        msg = form.errors

            else:
                msg = "this was not a meter_data csv file"

        elif request.POST['csv_type'] == 'half_hourly':
            if 'consumption,meter_id,reading_date_time' in lines[0]:
                for line in lines[1:]:
                    fields = line.split(",")
                    if fields[0] != '':
                        data_dict = {}
                        data_dict["consumption"] = fields[0]
                        data_dict["meter"] = fields[1]
                        data_dict["reading_date_time"] = fields[2]
                    try:
                        form = HalfhourlyDataForm(data_dict)
                        if form.is_valid():
                            form.save()
                            msg = "successfully uploaded half hourly reading data"
                        else:
                            msg = form.errors
                    except Exception as e:
                        msg = form.errors

            else:
                msg = "this was not a half-hourly data file"

        return render(request, "upload_csv/upload_csv.html", {"post_process_message": msg, 'error_dict': all_errors})


