from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url


urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', include('upload_csv.urls')),
    path('', include('data_view.urls'))
]
