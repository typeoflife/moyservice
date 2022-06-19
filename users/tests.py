"""Определяет схемы URL для пользователей"""

from django.urls import path, include

from users.views import register

app_name = 'users'
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', register, name='register')

]