"""Определяет схемы URL для learning_logs"""

from django.urls import path
from backend.views import index, orders, order, new_order, new_entry, edit_entry, all_cash, cash, new_cash

app_name = 'backend'
urlpatterns = [
    path('', index, name='index'),
    path('orders/', orders, name='orders'),
    path('orders/<int:order_id>/', order, name='order'),
    path('new_order/', new_order, name='new_order'),
    path('new_entry/<int:order_id>/', new_entry, name='new_entry'),
    path('edit_entry/<int:entry_id>/', edit_entry, name='edit_entry'),
    path('all_cash/', all_cash, name='all_cash'),
    path('all_cash/<int:cash_id>/', cash, name='cash'),
    path('new_cash/', new_cash, name='new_cash'),
]