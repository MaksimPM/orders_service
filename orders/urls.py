from django.urls import path

from orders.apps import OrdersConfig
from orders.views import (OrderCreateAPIView, OrderListAPIView, OrderDestroyAPIView, OrderUpdateAPIView,
                          OrderRetrieveAPIView, OrderListView, OrderCreateView, OrderDeleteView, OrderEditView, OrderStatusUpdateView, RevenueReportView)

app_name = OrdersConfig.name

urlpatterns = [
    path('api/add/', OrderCreateAPIView.as_view(),name='add_order_api'),
    path('api/list_orders/', OrderListAPIView.as_view(),name='order_list_api'),
    path('api/retrieve_order/<int:pk>/', OrderRetrieveAPIView.as_view(),name='retrieve_order_api'),
    path('api/edit_order/<int:pk>/', OrderUpdateAPIView.as_view(), name='edit_order_api'),
    path('api/delete_order/<int:pk>/', OrderDestroyAPIView.as_view(), name='delete_order_api'),

    path('', OrderListView.as_view(), name='order_list'),
    path('add/', OrderCreateView.as_view(), name='add_order'),
    path('delete/<int:pk>/', OrderDeleteView.as_view(), name='delete_order'),
    path('update_status/<int:order_id>/', OrderStatusUpdateView.as_view(), name='update_status'),
    path('edit/<int:pk>/', OrderEditView.as_view(), name='edit_order'),
    path('revenue/', RevenueReportView.as_view(), name='revenue_report'),
]
