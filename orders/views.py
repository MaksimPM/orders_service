from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import FormView
from rest_framework import viewsets, generics
from items.models import Item
from orders.models import Order
from orders.serializers import OrderSerializer
from orders.forms import OrderForm, OrderStatusForm, OrderEditForm
from django.db.models import Sum
from django.http import JsonResponse

"""API Эндпоинты для работы с заказом"""
class OrderCreateAPIView(generics.CreateAPIView):
    queryset = Order.objects.prefetch_related('items')
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        return order

class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items')
    serializer_class = OrderSerializer


class OrderRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Order.objects.prefetch_related('items')
    serializer_class = OrderSerializer


class OrderUpdateAPIView(generics.UpdateAPIView):
    queryset = Order.objects.prefetch_related('items')
    serializer_class = OrderSerializer


class OrderDestroyAPIView(generics.DestroyAPIView):
    queryset = Order.objects.prefetch_related('items')


"""Эндпоинт для вывода списка заказов"""
class OrderListView(ListView):
    model = Order
    template_name = "order_list.html"
    context_object_name = "orders"

    def get_queryset(self):
        status_filter = self.request.GET.get('status', '').strip()
        search_query = self.request.GET.get('search', '').strip()
        orders = Order.objects.prefetch_related('items')

        if status_filter:
            orders = orders.filter(status=status_filter)

        if search_query:
            if search_query.isdigit():
                orders = orders.filter(table_number=search_query)
            else:
                orders = orders.filter(status__icontains=search_query)

        return orders.order_by('id')

"""Эндпоинт для создания заказов"""
class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = "add_order.html"
    success_url = reverse_lazy("orders:order_list")

    def form_valid(self, form):
        order = form.save()
        order.update_total_price()
        messages.success(self.request, f"Заказ №{order.id} успешно создан")
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, "Пожалуйста, исправьте ошибки ниже.")
        return self.render_to_response(self.get_context_data(form=form, errors=form.get_errors()))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["items"] = Item.objects.all()
        return context

"""Эндпоинт для удаления заказов"""
class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy("orders:order_list")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

"""Эндпоинт для редактирования заказов"""
class OrderEditView(UpdateView):
    model = Order
    form_class = OrderEditForm
    template_name = "edit_order.html"
    success_url = reverse_lazy("orders:order_list")

    def form_valid(self, form):
        selected_items = self.request.POST.getlist("items")

        if not selected_items:
            messages.error(self.request, "Выберите хотя бы одно блюдо")
            return self.form_invalid(form)

        order = form.save()
        order.update_total_price()
        order.items.set(Item.objects.filter(id__in=selected_items))
        messages.success(self.request, f"Заказ №{order.id} успешно обновлен")
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, "Пожалуйста, исправьте ошибки ниже.")
        return self.render_to_response(self.get_context_data(form=form, errors=form.get_errors()))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["items"] = Item.objects.all()
        return context

"""Эндпоинт для обновления статуса заказов"""
@method_decorator(csrf_exempt, name='dispatch')
class OrderStatusUpdateView(FormView):
    form_class = OrderStatusForm

    def post(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=self.kwargs["order_id"])
        form = self.get_form()

        if form.is_valid():
            new_status = form.cleaned_data["status"]
            if new_status in ["pending", "ready", "paid"]:
                order.status = new_status
                order.save()
                return JsonResponse({"success": True})

        return JsonResponse({"success": False}, status=400)

"""Эндпоинт для рассчета выручки за смену"""
class RevenueReportView(View):
    template_name = "revenue_report.html"

    def get(self, request):
        paid_orders = Order.objects.filter(status='paid').prefetch_related('items')
        total_revenue = paid_orders.aggregate(total_revenue=Sum('total_price'))['total_revenue'] or 0
        return render(request, self.template_name, {'paid_orders': paid_orders, 'total_revenue': total_revenue})
