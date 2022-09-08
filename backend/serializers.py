from rest_framework import serializers

from backend.models import Order, Comment, Cash, Client


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['text', 'date_added']


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['fio', 'telephone', 'address']


class OrderSerializer(serializers.ModelSerializer):
    clients = ClientSerializer(many=True)
    comments = CommentSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'clients', 'status', 'device', 'model', 'serial_number', 'order_number', 'summ', 'text',
                  'comments', ]


class OrdersSerializer(serializers.ModelSerializer):
    clients = ClientSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = ['id', 'clients', 'status', 'device', 'model', 'serial_number', 'summ', 'order_number', ]
        # extra_kwargs = {'clients': {'required': True}}
        read_only_fields = ['status', 'order_number']


class OrderDoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_number', 'summ', 'text']
        extra_kwargs = {'summ': {'required': True}, 'text': {'required': True}}


class CashSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cash
        fields = ['id', 'name', 'money', ]
        read_only_fields = ['money']
