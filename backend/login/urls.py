from django.urls import path
from login import views

urlpatterns = [
    path('login', views.login),
    path('info', views.info),
    path('logout', views.logout),
]