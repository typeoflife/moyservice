from django.db import models
from account.models import User

STATUS = (
    ('open', 'Открыт'),
    ('close', 'Закрыт'),
)


class Order(models.Model):
    device = models.CharField(verbose_name='Устройство', max_length=100)
    model = models.CharField(verbose_name='Модель', max_length=100)
    serial_number = models.CharField(verbose_name='Серийный номер', max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    status = models.CharField(verbose_name='Статус заказа', choices=STATUS, max_length=5, default='open')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order')
    order_number = models.PositiveIntegerField()

    class Meta:
        verbose_name_plural = 'order'

    def __str__(self):
        return f'Заказ №{self.order_number}, ({self.device}), принят {self.date_added}'


class Comment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Комментарий')
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'comments'

    def __str__(self):
        return self.text


class Cash(models.Model):
    name = models.CharField(verbose_name='Название кассы', max_length=30)
    money = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cash')

    class Meta:
        verbose_name_plural = 'cash'

    def __str__(self):
        return f'{self.name}'