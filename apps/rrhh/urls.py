from apps.rrhh.views.employee_views import employees_list
from django.urls import path

urlpatterns = [
    path('employees-list/', employees_list, name='employees_list'),
]
