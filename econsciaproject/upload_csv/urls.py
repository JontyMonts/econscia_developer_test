from django.urls import path

urlpatterns = [
    path('', views.upload_csv, name='upload_csv'),
]
