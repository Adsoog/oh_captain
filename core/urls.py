from django.urls import path
from core.views import generic_search, comments

urlpatterns = [
    path('search-form/', generic_search, name='generic_search'),
    path('comments/<str:model_name>/<int:object_id>/', comments, name='get_comments'),
]
