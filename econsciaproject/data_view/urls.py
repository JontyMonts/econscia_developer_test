from django.urls import path
from .views import present_all_data, specific_building, specific_meter

urlpatterns = [
    path('', present_all_data, name='present_all_data'),
    path('building/', specific_building, name='specific_building'),
    path('meter/', specific_meter, name='specific_meter')
]
