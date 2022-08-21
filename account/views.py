from django.contrib.auth.password_validation import validate_password
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from account.models import new_user_registered, ConfirmEmailToken
from account.serializers import RegistrationUserSerializer


class RegisterAccount(APIView):
    """Для регистрации покупателей"""

    def post(self, request, *args, **kwargs):
        serializer = RegistrationUserSerializer(data=request.data)
        try:
            validate_password(request.data['password'])
        except Exception as password_error:
            error_array = []
            for item in password_error:
                error_array.append(item)
            return JsonResponse({'Status': False, 'Errors': {'password': error_array}})
        else:
            data = {}
            if serializer.is_valid():
                user = serializer.save()
                data['response'] = 'Пользователь зарегестрирован'
                data['email'] = user.email
                data['username'] = user.username
                new_user_registered.send(sender=self.__class__, user_id=user.id, email=user.email)
            else:
                data = serializer.errors
            return Response(data)


class AccountVerify(APIView):
    """Для подтверждения почтового адреса"""

    def post(self, request, *args, **kwargs):

        # проверяем обязательные аргументы
        if {'email', 'token'}.issubset(request.data):

            token = ConfirmEmailToken.objects.filter(user__email=request.data['email'],
                                                     key=request.data['token']).first()
            if token:
                token.user.is_active = True
                token.user.save()
                token.delete()
                return JsonResponse({'Status': True})
            else:
                return JsonResponse({'Status': False, 'Errors': 'Неправильно указан токен или email'})

        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

