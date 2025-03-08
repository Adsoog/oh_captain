from django.urls import path
from core.views import generic_search

urlpatterns = [
    path('search-form/', generic_search, name='generic_search'),
]
