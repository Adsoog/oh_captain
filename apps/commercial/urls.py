from django.urls import path
from apps.commercial.views.client_views import clients_list, client_create, client_detail, client_delete, client_edit, \
    client_branch_edit, client_branch_delete, client_branch_create, client_contact_create, client_contact_edit, \
    client_contact_delete
from apps.commercial.views.equipment_views import proforma_equipment_add, proforma_equipment_edit, \
    proforma_equipment_edit_all, proforma_equipment_delete
from apps.commercial.views.instrument_views import instruments_list, InstrumentListView, upload_instruments_list, \
    instrument_detail, download_instruments_list
from apps.commercial.views.proforma_views import proformas_list, proforma_detail, auto_proforma_create, proforma_delete, \
    proforma_edit, branch

urlpatterns = []

clientpatterns = [
    path('client/list/', clients_list, name='clients_list'),
    path('client/create/', client_create, name='client_create'),
    path('client/detail/<int:id>/', client_detail, name='client_detail'),
    path('client/delete/<int:id>/', client_delete, name='client_delete'),
    path('client/edit/<int:id>/', client_edit, name='client_edit'),
    # BRANCH PATTERNS
    path('client-detail/edit-branch/<int:id>/', client_branch_edit, name='client_branch_edit'),
    path('client-detail/delete-branch/<int:id>/', client_branch_delete, name='client_branch_delete'),
    path('client-detail/add-branch/<int:id>/', client_branch_create, name='client_branch_create'),
    # CONTACT PATTERNS
    path('client/detail/add-contact/<int:id>/', client_contact_create, name='client_contact_create'),
    path('client/detail/edit-contact/<int:id>/', client_contact_edit, name='client_contact_edit'),
    path('client/detail/delete-contact/<int:id>/', client_contact_delete, name='client_contact_delete'),
]

instrumentpatterns = [
    path('instruments/list/', instruments_list, name='instruments_list'),
    path('instruments-class/list/', InstrumentListView.as_view(), name='class_instruments_list'),
    path('instruments/detail/<int:id>/', instrument_detail, name='instrument_detail'),
    path('instruments/upload/list/', upload_instruments_list, name='upload_instruments_list'),
    path('instruments/dowload/list/', download_instruments_list, name='download_instruments_list'),
]

proformapatterns = [
    path('proforma/list/', proformas_list, name='proformas_list'),
    path('proforma/create/', auto_proforma_create, name='auto_proforma_create'),
    path('proforma/detail/<int:id>/', proforma_detail, name='proforma_detail'),
    path('proforma/delete/<int:id>/', proforma_delete, name='proforma_delete'),
    path('proforma/edit/<int:id>/', proforma_edit, name='proforma_edit'),
    path('branch/', branch, name='branch'),
    # EQUIPMENT
    path('proforma/detail/add-equipment/<int:id>/', proforma_equipment_add, name='proforma_equipment_add'),
    path('proforma/detail/edit-equipment/<int:id>/', proforma_equipment_edit, name='proforma_equipment_edit'),
    path('proforma/detail/edit-all-equipment/<int:id>/', proforma_equipment_edit_all,
         name='proforma_equipment_edit_all'),
    path('proforma/detail/delete-equipment/<int:id>/', proforma_equipment_delete, name='proforma_equipment_delete'),
]

urlpatterns += clientpatterns
urlpatterns += instrumentpatterns
urlpatterns += proformapatterns
