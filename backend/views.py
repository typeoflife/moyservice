from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from backend.models import Order, Comment
from backend.serializers import OrderSerializer, CommentSerializer
from rest_framework.response import Response


class OrderViewset(viewsets.ModelViewSet):
    """Viewset для заказов"""

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(user_id=self.request.user.id).order_by('-order_number')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        counter = Order.objects.filter(user_id=self.request.user.id).count() + 1
        serializer.save(user_id=self.request.user.id, order_number=counter)


class CommentView(APIView):
    """Добавление коментариев"""

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Необходима аунтификация'}, status=403)
        if {'order_id', 'text'}.issubset(request.data):

            order = Order.objects.filter(
                user_id=request.user.id, status='open', order_number=request.data['order_id'])

            if order:
                serializer = CommentSerializer(data=request.data)
                print(serializer)
                serializer.is_valid(raise_exception=True)
                serializer.save(text=self.request.data['text'],
                                order_id=request.data['order_id'], user_id=request.user.id)
            else:
                return JsonResponse({'Status': False, 'Errors': 'Заказ не найден, либо закрыт'})
            return Response('123')
        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})
