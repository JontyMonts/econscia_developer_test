from django.urls import path
from .views import present_all_data

urlpatterns = [
    path('', present_all_data, name='present_all_data'),
]
