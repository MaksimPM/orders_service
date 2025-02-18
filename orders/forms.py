from django import forms

from items.models import Item
from .models import Order

"""Форма для создания заказа"""
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['table_number', 'items']

    items = forms.ModelMultipleChoiceField(
        queryset=Item.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Выберите блюда"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['items'].error_messages = {
            'required': 'Пожалуйста, выберите хотя бы одно блюдо!',
        }

    def get_errors(self):
        error_messages = {}
        for field, errors in self.errors.items():
            error_messages[field] = [self._get_custom_error_message(error) for error in errors]
        return error_messages

    def _get_custom_error_message(self, error):
        if error == 'This field is required.':
            return 'Это поле обязательно для заполнения!'
        return error

"""Форма для редактирования заказа"""
class OrderEditForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['items']

    items = forms.ModelMultipleChoiceField(
        queryset=Item.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Выберите блюда"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['items'].error_messages = {
            'required': 'Пожалуйста, выберите хотя бы одно блюдо!',
        }

    def get_errors(self):
        error_messages = {}
        for field, errors in self.errors.items():
            error_messages[field] = [self._get_custom_error_message(error) for error in errors]
        return error_messages

    def _get_custom_error_message(self, error):
        if error == 'This field is required.':
            return 'Это поле обязательно для заполнения!'
        return error

class OrderStatusForm(forms.Form):
    STATUS_CHOICES = [
        ('pending', 'Ожидание'),
        ('ready', 'Готов'),
        ('paid', 'Оплачен')
    ]
    status = forms.ChoiceField(choices=STATUS_CHOICES)
