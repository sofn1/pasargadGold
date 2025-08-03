from rest_framework import serializers
from .models import CartItem, Order, OrderItem
from products.models.product import Product


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'
        read_only_fields = ['user']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'total_price', 'status', 'address', 'location', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user

        order = Order.objects.create(user=user, **validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order
