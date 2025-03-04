from apps.requests.views.request_views import requests_list
from django.urls import path

urlpatterns = [
    path('list/', requests_list, name='requests_list'),
]
