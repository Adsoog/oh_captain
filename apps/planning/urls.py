from django.urls import path

from apps.planning.views.workorder_views import work_orders_list, work_order_detail, work_order_delete, work_order_edit

urlpatterns = [
    path('orders/list/', work_orders_list, name="work_orders_list"),
    path('orders/detail/<int:id>/', work_order_detail, name="work_order_detail"),
    path('orders/edit/<int:id>/', work_order_edit, name="work_order_edit"),
    path('orders/delete/<int:id>/', work_order_delete, name="work_order_delete"),

]
