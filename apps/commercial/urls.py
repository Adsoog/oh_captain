from django.urls import path
from apps.commercial.views.client_views import clients_list, client_create, client_detail, client_delete, client_edit, client_branch_edit, client_branch_delete, client_branch_create
from apps.commercial.views.instrument_views import instruments_list, InstrumentListView

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
]

instrumentpatterns = [
    path('instruments/list/', instruments_list, name='instruments_list'),
    path('instruments-class/list/', InstrumentListView.as_view(), name='class_instruments_list'),
]

urlpatterns += clientpatterns
urlpatterns += instrumentpatterns
