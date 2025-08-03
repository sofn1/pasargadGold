from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CartItem, Order, OrderItem
from .serializers import CartItemSerializer, OrderSerializer
from .zarinpal_client import ZarinpalGateway
from django.shortcuts import redirect
from django.conf import settings


class CartItemView(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CartItemDeleteView(generics.DestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)


class CreateOrderView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        order = serializer.save(user=self.request.user)
        # Optionally clear cart
        CartItem.objects.filter(user=self.request.user).delete()


class PayWithZarinpal(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, order_id):
        order = Order.objects.get(pk=order_id, user=request.user)
        gateway = ZarinpalGateway(merchant_id="your-merchant-id", sandbox=True)
        result = gateway.request_payment(order.total_price, f'Order #{order.id}', settings.ZARINPAL_CALLBACK,
                                         request.user.phone_number)

        if result.get('status') == 100:
            order.authority = result['authority']
            order.save()
            return Response({"redirect": result['url']})
        return Response({"detail": "Zarinpal error"}, status=400)


class ZarinpalVerify(APIView):
    def get(self, request):
        authority = request.GET.get('Authority')
        status_param = request.GET.get('Status')

        try:
            order = Order.objects.get(authority=authority)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found"}, status=404)

        gateway = ZarinpalGateway()
        result = gateway.verify_payment(order.total_price, authority)

        if result.get('status') == 100:
            order.status = 'paid'
            order.save()
            return redirect(settings.ZARINPAL_SUCCESS_URL)  # redirect to thank you page
        else:
            order.status = 'failed'
            order.save()
            return redirect(settings.ZARINPAL_FAIL_URL)  # redirect to fail page
