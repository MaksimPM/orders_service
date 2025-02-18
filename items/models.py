from django.db import models

class Item(models.Model):
    title = models.CharField(max_length=200, verbose_name='наименование')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='стоимость')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'блюдо'
        verbose_name_plural = 'блюда'
