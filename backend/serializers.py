from rest_framework import serializers
from rest_framework.relations import StringRelatedField

from backend.models import Order, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['order_id', 'text', 'date_added']


class OrderSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = Order
        fields = ['id', 'status', 'device', 'model', 'serial_number', 'order_number', 'comment']
        read_only_fields = ['status', 'order_number']
