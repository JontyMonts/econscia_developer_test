from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from upload_csv import views # do we need this?

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', include('upload_csv.urls')),
    path('view/', include('data_view.urls'))
]
