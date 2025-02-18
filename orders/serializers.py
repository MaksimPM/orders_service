from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    table_number = serializers.IntegerField(
        required=True,
        error_messages={
            'invalid': 'Номер стола должен быть числом!',
            'required': 'Номер стола обязателен для заполнения!'
        }
    )

    items = serializers.PrimaryKeyRelatedField(
        queryset=Order.items.rel.model.objects.all(),
        many=True,
        allow_empty=False,
        error_messages={
            'empty': 'Необходимо добавить хотя бы одно блюдо!',
            'required': 'Поле "items" обязательно для заполнения!'
        }
    )
