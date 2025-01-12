from django.urls import path
from grade import views

urlpatterns = [
    path('grade_list', views.grade_list),
    path('grade_edit', views.grade_edit),
    path('grade_delete', views.grade_delete),
    path('role_list', views.role_list),
]