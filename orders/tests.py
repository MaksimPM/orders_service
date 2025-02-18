from django.test import TestCase
from django.contrib.messages import get_messages
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Order, Item
from django.urls import reverse


class OrderTests(TestCase):

    def setUp(self):
        self.item1 = Item.objects.create(title="Item 1", price=100)
        self.item2 = Item.objects.create(title="Item 2", price=200)
        self.order = Order.objects.create(table_number=1, status='pending')
        self.order.items.add(self.item1, self.item2)

    def test_order_list_view_get(self):
        url = reverse('orders:order_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order_list.html')
        self.assertIn('orders', response.context)

    def test_order_create_view_post_valid_data(self):
        url = reverse('orders:add_order')
        data = {
            'table_number': 2,
            'items': [self.item1.id, self.item2.id]
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('orders:order_list'))

        messages = list(get_messages(response.wsgi_request))
        order_id = Order.objects.latest('id').id
        self.assertEqual(str(messages[0]), f'Заказ №{order_id} успешно создан')

    def test_order_create_view_post_invalid_data(self):
        url = reverse('orders:add_order')
        data = {
            'table_number': 2,
            'items': []
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertIn('Пожалуйста, выберите хотя бы одно блюдо!', form.errors.get('items', []))

    def test_order_delete_view_get(self):
        url = reverse('orders:delete_order', args=[self.order.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('orders:order_list'))

    def test_order_edit_view_post_valid_data(self):
        url = reverse('orders:edit_order', args=[self.order.id])
        data = {
            'items': [self.item1.id]
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('orders:order_list'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), f'Заказ №{self.order.id} успешно обновлен')

    def test_order_status_update_view_post_valid_data(self):
        url = reverse('orders:update_status', args=[self.order.id])
        data = {'status': 'ready'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content.decode(), {'success': True})

        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'ready')

    def test_order_status_update_view_post_invalid_data(self):
        url = reverse('orders:update_status', args=[self.order.id])
        data = {'status': 'invalid_status'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)

        self.assertJSONEqual(response.content.decode(), {'success': False})

    def test_revenue_report_view_get(self):
        url = reverse('orders:revenue_report')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'revenue_report.html')
        self.assertIn('total_revenue', response.context)


class OrderAPITests(APITestCase):
    def setUp(self):
        self.item1 = Item.objects.create(title='Блюдо 1', price=100)
        self.item2 = Item.objects.create(title='Блюдо 2', price=200)
        self.item3 = Item.objects.create(title='Блюдо 3', price=150)
        self.order = Order.objects.create(table_number=1)
        self.order.items.add(self.item1, self.item2)
        self.url = reverse('orders:order_list_api')

    def test_create_order(self):
        url = reverse('orders:add_order_api')
        data = {
            'table_number': 2,
            'items': [self.item1.id, self.item2.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_order_invalid_data(self):
        url = reverse('orders:add_order_api')
        data = {
            'table_number': -1,  # Неверный номер стола
            'items': [self.item1.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Номер стола должен быть положительным', str(response.data))

    def test_list_orders(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_order(self):
        url = reverse('orders:retrieve_order_api', kwargs={'pk': self.order.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['table_number'], self.order.table_number)

    def test_update_order(self):
        url = reverse('orders:edit_order_api', kwargs={'pk': self.order.pk})
        data = {
            'table_number': 3,
            'items': [self.item1.id],
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.table_number, 3)

    def test_delete_order(self):
        url = reverse('orders:delete_order_api', kwargs={'pk': self.order.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.count(), 0)

    def test_order_total_price_update_on_item_add(self):
        new_item = Item.objects.create(title='Блюдо 3', price=150)
        url = reverse('orders:edit_order_api', kwargs={'pk': self.order.pk})
        data = {
            'table_number': self.order.table_number,
            'items': [self.item1.id, self.item2.id, new_item.id],
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(str(self.order.total_price), '450.00')

    def test_order_total_price_update_on_item_remove(self):
        url = reverse('orders:edit_order_api', kwargs={'pk': self.order.pk})
        data = {
            'table_number': self.order.table_number,
            'items': [self.item1.id],  # Убираем второе блюдо
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(str(self.order.total_price), '100.00')
