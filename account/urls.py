from django.urls import path
from django_rest_passwordreset.views import reset_password_request_token, reset_password_confirm
from rest_framework.authtoken import views

from account.views import RegisterAccount, AccountVerify

app_name = 'account'

urlpatterns = [
    path('login/', views.obtain_auth_token),
    path('register/', RegisterAccount.as_view(), name='register'),
    path('password_reset/', reset_password_request_token, name='password-reset'),
    path('password_reset/confirm', reset_password_confirm, name='password-reset-confirm'),
    path('account-verify', AccountVerify.as_view(), name='account-verify')

]