from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    # Api
    path('api/user/', include('user.urls')),
    # path('api/v1/', include('djoser.urls')),
    # path('api/v1/', include('product.urls')),
    # path('api/v1/', include('order.urls')),
]

