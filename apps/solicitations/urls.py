from apps.solicitations.views.solicitation_views import solicitations_list, auto_solicitation_create, solicitation_detail
from django.urls import path

urlpatterns = [
    path('list/', solicitations_list, name='solicitations_list'),
    path('detail/<int:pk>/', solicitation_detail, name='solicitation_detail'),
    path('create/', auto_solicitation_create, name='auto_solicitation_create'),

]
