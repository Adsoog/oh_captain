from apps.solicitations.views.exit_ticket_views import exit_ticket_detail
from apps.solicitations.views.expense_views import expense_detail, expense_item_edit, expense_item_create, \
    expense_item_delete
from apps.solicitations.views.mobility_views import mobility_sheet_detail, mobility_item_create, mobility_item_delete
from apps.solicitations.views.petty_cash_views import petty_cash_detail
from apps.solicitations.views.solicitation_views import solicitations_list, auto_solicitation_create, \
    solicitation_detail, solicitation_delete, solicitation_edit, solicitation_type_form
from apps.solicitations.views.perdiem_request_views import perdiem_request_detail
from django.urls import path

urlpatterns = []

solicitationpatterns = [
    path('list/', solicitations_list, name='solicitations_list'),
    path('detail/<int:pk>/', solicitation_detail, name='solicitation_detail'),
    path('delete/<int:pk>/', solicitation_delete, name='solicitation_delete'),
    path('create/', auto_solicitation_create, name='auto_solicitation_create'),
    path('detail/type/<int:pk>/', solicitation_type_form, name='solicitation_type_form'),
    path('detail/edit/<int:pk>/', solicitation_edit, name='solicitation_edit'),
]

perdiempatterns = [
    path('perdiems/detail/<int:pk>', perdiem_request_detail, name='perdiem_request_detail')
]

exit_ticketpatterns = [
    path('exit_ticket/detail/<int:pk>/', exit_ticket_detail, name='exit_ticket_detail'),
]

expensespatterns = [
    path('expenses/detail/<int:pk>/', expense_detail, name='expenses_detail'),
    path('expenses/detail/item/add/<int:pk>/', expense_item_create, name='expense_item_create'),
    path('expenses/detail/item/edit/<int:pk>/', expense_item_edit, name='expense_item_edit'),
    path('expenses/detail/item/delete/<int:pk>/', expense_item_delete, name='expense_item_delete'),
]

pettycashpatterns = [
    path('petty_cash/detail/<int:pk>/', petty_cash_detail, name='petty_cash_detail'),
]

mobilitysheetpatterns = [
    path('mobility_sheet/detail/<int:pk>/', mobility_sheet_detail, name='mobility_sheet_detail'),
    path('mobility_sheet/detail/create/<int:pk>/', mobility_item_create, name='mobility_item_create'),
    path('mobility_sheet/detail/delete/<int:pk>/', mobility_item_delete, name='mobility_item_delete'),
]

urlpatterns += solicitationpatterns
urlpatterns += perdiempatterns
urlpatterns += exit_ticketpatterns
urlpatterns += expensespatterns
urlpatterns += pettycashpatterns
urlpatterns += mobilitysheetpatterns
