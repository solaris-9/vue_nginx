from django.urls import path
from customer import views

urlpatterns = [
    path('list', views.list),
    path('edit', views.edit),
    #path('delete', views.delete),
]