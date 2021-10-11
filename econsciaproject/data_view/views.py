from django.shortcuts import render

# Create your views here.

def present_data(request):
    return render(request, "data_view/showdata.html", {})
