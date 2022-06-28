from django.contrib.auth.models import User
from django.db import models

STATE = (
    ('open', 'Открыт'),
    ('close', 'Закрыт'),
)


class Order(models.Model):
    device = models.CharField(verbose_name='Устройство', max_length=100)
    model = models.CharField(verbose_name='Модель', max_length=100)
    serial_number = models.CharField(verbose_name='Серийный номер', max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    state = models.CharField(verbose_name='Статус заказа', choices=STATE, max_length=5, default='open')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topic')
    order_number = models.PositiveIntegerField(default=1)

    # перед сохранением обьекта делаем проверку, если у пользователя заказы уже есть, то к последнему прибавляем +1
    def save(self, *args, **kwargs):
        self.object_list = Order.objects.filter(owner_id=self.owner)
        if len(self.object_list) == 0:
            self.order_number = 1
        else:
            self.order_number = self.object_list.last().order_number + 1
        super(Order, self).save()

    def __str__(self):
        return f'Заказ № {self.order_number}'


class Entry(models.Model):
    """Информация изученная пользователем по теме"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='entry')
    text = models.TextField(verbose_name='Комментарий')
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        """Возвращает строковое представление модели"""
        if len(self.text) > 50:
            return f'{self.text[:50]}...'
        return self.text


class Cash(models.Model):
    name = models.CharField(verbose_name='Название кассы',max_length=30)
    money = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cash')

    class Meta:
        verbose_name_plural = 'cash'

    def __str__(self):
        return f'{self.name}'