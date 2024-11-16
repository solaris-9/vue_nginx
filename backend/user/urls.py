from django.urls import path
from user import views

urlpatterns = [
    path('login', views.login),
    path('info', views.info),
    path('grade_manage', views.grade_manage),
]