from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('completed', 'Выполнен'),
        ('cancelled', 'Отменён'),
    ]

    client = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='orders', verbose_name='Клиент'
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='orders', verbose_name='Товар'
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус'
    )
    notes = models.TextField(blank=True, verbose_name='Примечания')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ #{self.pk} — {self.client.username} — {self.product.name}'

    @property
    def total_price(self):
        return self.product.final_price * self.quantity
