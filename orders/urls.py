from django.urls import path, include
from rest_framework.routers import DefaultRouter

from orders.apps import OrdersConfig
from orders.views import (OrderViewSet, OrderListView, OrderCreateView, OrderDeleteView,
                          OrderEditView, OrderStatusUpdateView, RevenueReportView)

app_name = OrdersConfig.name

router = DefaultRouter()
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', OrderListView.as_view(), name='order_list'),
    path('add/', OrderCreateView.as_view(), name='add_order'),
    path('delete/<int:pk>/', OrderDeleteView.as_view(), name='delete_order'),
    path('update_status/<int:order_id>/', OrderStatusUpdateView.as_view(), name='update_status'),
    path('edit/<int:pk>/', OrderEditView.as_view(), name='edit_order'),
    path('revenue/', RevenueReportView.as_view(), name='revenue_report'),
] + router.urls
