from django.shortcuts import render

# Create your views here.
def upload_csv(request):
    if "GET" == request.method:
        return render(request, "upload_csv.html", {})

    elif "POST" == request.method:
        pass
        # Handle csv data