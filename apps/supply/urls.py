from django.urls import path

from apps.supply.views.asset_request import asset_request, approve_request, reject_request
from apps.supply.views.asset_views import assets_list, asset_detail, asset_delete, asset_create_edit, asset_attribute

urlpatterns = []

assetpatterns = [
    path('asset/', assets_list, name='assets_list'),
    path('asset/detail/<int:id>/', asset_detail, name='asset_detail'),
    path('asset/delete/<int:id>/', asset_delete, name='asset_delete'),
    path('asset/create/', asset_create_edit, name='asset_create'),
    path('asset/edit/<int:id>/', asset_create_edit, name='asset_edit'),
    path('asset/attribute/<int:asset_id>/', asset_attribute, name='asset_attribute'),

    # prueba
    path('asset/request/', asset_request, name='asset_request'),
    path("request/<int:request_id>/approve/", approve_request, name="approve_request"),
    path("request/<int:request_id>/reject/", reject_request, name="reject_request"),

]

urlpatterns += assetpatterns
