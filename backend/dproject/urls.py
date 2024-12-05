from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin as adm
from django.urls import path, include

urlpatterns = [
    # Admin
    path('api/grade/', include('grade.urls')),
    # Api
    path('api/user/', include('user.urls')),
]

