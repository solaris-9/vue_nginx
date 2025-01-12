from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin as adm
from django.urls import path, include

urlpatterns = [
    # Login
    path('api/login/', include('login.urls')),
    # User
    path('api/user/', include('user.urls')),
    # Grade
    path('api/grade/', include('grade.urls')),
    # Common
    path('api/common/', include('common.urls')),
    # DeviceDP
    path('api/devicedp/', include('devicedp.urls')),
    # Customer
    path('api/customer/', include('customer.urls')),
    # Platform
    path('api/platform/', include('cplatform.urls')),
    # Nwcc
    path('api/nwcc/', include('nwcc.urls')),
]

