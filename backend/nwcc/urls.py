from django.urls import path
from nwcc import views

urlpatterns = [
    path('list', views.list),
    path('edit', views.edit),
    path('delete', views.delete),
]