from django.urls import path
from apps.supply.views.asset_views import assets_list, asset_detail, asset_delete, asset_create_edit, asset_attribute

urlpatterns = []

assetpatterns = [
    path('asset/', assets_list, name='assets_list'),
    path('asset/detail/<int:id>/', asset_detail, name='asset_detail'),
    path('asset/delete/<int:id>/', asset_delete, name='asset_delete'),
    path('asset/create/', asset_create_edit, name='asset_create'),
    path('asset/edit/<int:id>/', asset_create_edit, name='asset_edit'),
    path('asset/attribute/<int:asset_id>/', asset_attribute, name='asset_attribute'),
]

urlpatterns += assetpatterns
