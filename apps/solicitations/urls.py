from apps.solicitations.views.solicitation_views import solicitations_list, auto_solicitation_create, \
    solicitation_detail, solicitation_delete, solicitation_edit
from django.urls import path

urlpatterns = [
    path('list/', solicitations_list, name='solicitations_list'),
    path('detail/<int:pk>/', solicitation_detail, name='solicitation_detail'),
    path('delete/<int:pk>/', solicitation_delete, name='solicitation_delete'),
    path('create/', auto_solicitation_create, name='auto_solicitation_create'),

]

solicitationpatterns = [
    path('detail/edit/<int:pk>/', solicitation_edit, name='solicitation_edit'),

]

urlpatterns += solicitationpatterns
