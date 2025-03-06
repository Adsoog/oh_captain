from django.urls import path
from apps.rrhh.views.employee_views import employees_list
from apps.rrhh.views.hierarchy_views import employee_hierarchy, assign_hierarchy, employee_hierarchy_detail

urlpatterns = []

employeepatterns = [
    path('employees-list/', employees_list, name='employees_list'),
]

hierarchypatterns = [
    path('employee/hierarchy/', employee_hierarchy, name='employee_hierarchy'),
    path('employee/assign-hierarchy/<int:employee_id>/', assign_hierarchy, name='assign_hierarchy'),
    path('employee/hierarchy-detail/<int:employee_id>/', employee_hierarchy_detail, name='employee_hierarchy_detail'),

]

urlpatterns += employeepatterns
urlpatterns += hierarchypatterns