from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from backend.models import Order, Cash
from backend.serializers import CommentSerializer, OrdersSerializer, OrderSerializer, CashSerializer, \
    OrderDoneSerializer, ClientSerializer
from rest_framework.response import Response


class OrdersViewset(viewsets.ModelViewSet):
    """Viewset для заказов"""

    queryset = Order.objects.all()
    serializer_class = OrdersSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(user_id=self.request.user.id).order_by('-order_number')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = OrderSerializer(instance)
        return Response(serializer.data)

    # создаем заказ и клиента одним запросом
    def create(self, request, *args, **kwargs):
        if {'fio', 'telephone'}.issubset(request.data):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            counter = Order.objects.filter(user_id=self.request.user.id).count() + 1
            order = serializer.save(user_id=self.request.user.id, order_number=counter)
            serializer = ClientSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(fio=serializer.validated_data['fio'], telephone=serializer.validated_data['telephone'],
                            order_id=order.id, user_id=request.user.id)
            return Response({'Status': True, 'Заказ': 'Создан'})
        else:
            return JsonResponse({'Status': False, 'Errors': 'Не указаны ФИО или телефон'})


class CashViewset(viewsets.ModelViewSet):
    """Viewset для кассы"""

    queryset = Cash.objects.all()
    serializer_class = CashSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(user_id=self.request.user.id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)


class CommentView(APIView):
    """View для коментариев"""
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Находим заказ по введеному order_number
        order = get_object_or_404(Order, user_id=request.user.id,
                                  order_number=request.data['order'])
        if order:
            serializer.save(text=serializer.validated_data['text'],
                            order_id=order.id, user_id=request.user.id)
        else:
            return JsonResponse({'Status': False, 'Errors': 'Заказ не найден, либо закрыт'})

        return Response({'Status': True, 'Комментарий': 'Создан'})


class OrderDoneView(APIView):
    """View для обьявления готовности заказа"""
    permission_classes = [IsAuthenticated]

    # меняем статус заказа, вносим сумму и информацию о работе
    def post(self, request, *args, **kwargs):
        serializer = OrderDoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = Order.objects.exclude(status='close').filter(
            user_id=request.user.id, order_number=serializer.validated_data['order_number'])
        if len(order) > 0:
            order.update(status='done', summ=serializer.validated_data['summ'], text=serializer.validated_data['text'])
            return JsonResponse({'Status': True, 'Заказ': 'Готов'})
        else:
            return JsonResponse({'Status': False, 'Errors': 'Заказ не найден, либо закрыт'})


class CloseOrderView(APIView):
    """View для закрытия заказа"""
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        order_number = request.data.get('order_number')
        cash_id = request.data.get('cash_id')
        if order_number and cash_id:
            order = Order.objects.exclude(status='close').filter(
                user_id=request.user.id, order_number=order_number)
            if len(order) > 0:
                cash = Cash.objects.filter(user_id=request.user.id, id=cash_id)
                if len(cash) > 0:
                    order_summ = Order.objects.exclude(status='close').filter(
                        user_id=request.user.id, order_number=order_number).values_list('summ', flat=True)[0]
                    cash_money = Cash.objects.filter(
                        user_id=request.user.id, id=cash_id).values_list('money', flat=True)[0]
                    cash.update(money=cash_money + order_summ)
                    order.update(status='close')
                    return JsonResponse({'Status': True, 'Заказ': 'Закрыт'})
                return JsonResponse({'Status': False, 'Error': 'Нет такой кассы'})
            else:
                return JsonResponse({'Status': False, 'Errors': 'Заказ не найден, либо закрыт'})

        return JsonResponse({'Status': False, 'Errors': 'Не указан номер заказа либо касса'})
