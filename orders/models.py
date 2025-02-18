from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from items.models import Item

"""Модель заказа"""
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('ready', 'Готово'),
        ('paid', 'Оплачено'),
    ]

    table_number = models.IntegerField(validators=[MinValueValidator(1)], verbose_name='номер стола')
    items = models.ManyToManyField(Item, verbose_name='блюда')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='сумма заказа')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name='статус заказа')

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new or self.pk:
            self.update_total_price()

    def update_total_price(self):
        total = self.items.aggregate(models.Sum('price'))['price__sum'] or 0
        self.total_price = total
        super().save(update_fields=["total_price"])

    def __str__(self):
        return f"Заказ {self.id} - Стол {self.table_number}"

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'


@receiver(m2m_changed, sender=Order.items.through)
def update_order_total(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        instance.update_total_price()
