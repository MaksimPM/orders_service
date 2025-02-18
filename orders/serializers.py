from rest_framework import serializers
from .models import Order, Item

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
        queryset=Item.objects.all(),
        many=True,
        allow_empty=False,
        error_messages={
            'empty': 'Необходимо добавить хотя бы одно блюдо!',
            'required': 'Поле "items" обязательно для заполнения!'
        }
    )

    def validate_table_number(self, value):
        if value <= 0:
            raise serializers.ValidationError("Номер стола должен быть положительным!")
        return value

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("Необходимо добавить хотя бы одно блюдо.")
        return value
