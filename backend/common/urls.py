from django.urls import path
from common import views

urlpatterns = [
    path('customer_list', views.customer_list),
    path('device_list', views.device_list),
    path('nwcc_list', views.nwcc_list),
    path('country_list', views.country_list),
    path('hosting_list', views.hosting_list),
    path('upload', views.upload),
    path('download', views.download),
]