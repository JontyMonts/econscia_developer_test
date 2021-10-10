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
        print("this is get")
        print(request.GET)
        return render(request, "upload_csv/upload_csv.html", {})


    elif "POST" == request.method:

        csv_file = request.FILES['csv_file']
        file_data = csv_file.read().decode('utf-8')
        lines = file_data.split("\r\n")
        print(lines)
        msg = "Error somewhere"

        # 3 different file processing

        if request.POST['csv_type'] == 'building':

            # check that the column names match to the building table
            assert 'id,name' in lines[0], "this was not a building csv file"

            for line in lines:
                # check that the line has data in it, as there are empty lines at the bottom of the file
                fields = line.split(",")
                if fields[0] != '':
                    data_dict = {}
                    data_dict["id"] = fields[0]
                    data_dict["name"] = fields[1]
                    print("data dict is \n" , data_dict)

                    # Save the row to the database 
                    try:
                        form = BuildingForm(data_dict)
                        if form.is_valid():
                            form.save()
                            msg = "successfully uploaded building data"

                    except Exception as e:
                        msg = "Failed to upload meter data"


        elif request.POST['csv_type'] == 'meter':
            assert 'building_id,id,fuel,unit' in lines[0], "this was not a meter_data csv file"
            # we don't want the top line
            for line in lines[1:]:
                fields = line.split(",")
                if fields[0] != '':
                    data_dict = {}
                    data_dict["building_id"] = fields[0]
                    data_dict["meter_id"] = fields[1]
                    data_dict["fuel"] = fields[2]
                    data_dict["unit"] = fields[3]
                try:
                    form = MeterDataForm(data_dict)
                    if form.is_valid():
                        form.save()
                        msg = "successfully uploaded meter data"

                except Exception as e:
                    msg = "Failed to upload meter data"

        elif request.POST['csv_type'] == 'half_hourly':
            for line in lines[1:]:
                fields = line.split(",")
                if fields[0] != '':
                    data_dict = {}
                    data_dict["consumption"] = fields[0]
                    data_dict["meter_id"] = fields[1]
                    data_dict["reading_date_time"] = fields[2]
                try:
                    form = HalfhourlyDataForm(data_dict)
                    print("validating form")
                    if form.is_valid():
                        form.save()
                        print("half hourly form saved")
                        msg = "successfully uploaded half hourly reading data"
                    else:
                        print("didn't work")
                        msg = form.errors

                except Exception as e:
                    print("error saving half hourly form")
                    print(e)
                    msg = form.errors

        
        return render(request, "upload_csv/upload_csv.html", {"post_process_message": msg})


