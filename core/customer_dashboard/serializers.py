from rest_framework import serializers
from orders.models import Order, OrderItem
from customer_dashboard.models import WishlistItem, Notification, Address, SupportTicket, TicketReply


class WishlistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistItem
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSummarySerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, source='orderitem_set')

    class Meta:
        model = Order
        fields = ['id', 'customer', 'status', 'created_at', 'items']


class SupportTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportTicket
        fields = '__all__'


class TicketReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketReply
        fields = '__all__'
