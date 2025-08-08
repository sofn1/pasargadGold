from django.views import View
from reportlab.pdfgen import canvas
from orders.models import OrderItem
from django.http import HttpResponse
from rest_framework.views import APIView
from orders.models import Order, CartItem
from products.models.product import Product
from rest_framework.response import Response
from django.shortcuts import render, redirect
from orders.serializers import OrderSerializer
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.permissions import IsAdminUser
from accounts.permissions import IsAdminOrSuperAdmin
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.generics import ListAPIView, UpdateAPIView
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import WishlistItem, Address, Notification, SupportTicket, TicketReply
from .serializers import (
    WishlistItemSerializer, AddressSerializer,
    NotificationSerializer, CartItemSerializer, OrderSummarySerializer,
    SupportTicketSerializer, TicketReplySerializer)

User = get_user_model()


@login_required
@user_passes_test(lambda u: u.role == 'customer')
def customer_dashboard_home(request):
    return render(request, 'customer_dashboard/dashboard.html')


class OrderHistoryPage(LoginRequiredMixin, View):
    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        return render(request, "customer_dashboard/order_history.html", {"orders": orders})


class ProfilePage(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "customer_dashboard/profile.html", {"user": request.user})


class RecommendedProductsPage(LoginRequiredMixin, View):
    def get(self, request):
        ordered_ids = OrderItem.objects.values_list('product_id', flat=True)
        recommended = Product.objects.filter(id__in=ordered_ids).distinct()[:10]
        return render(request, "customer_dashboard/recommended.html", {"recommended": recommended})


class WishlistPage(LoginRequiredMixin, View):
    def get(self, request):
        items = WishlistItem.objects.filter(customer=request.user.customer)
        return render(request, "customer_dashboard/wishlist.html", {"items": items})


class CartPage(LoginRequiredMixin, View):
    def get(self, request):
        cart_items = CartItem.objects.filter(user=request.user)
        return render(request, "customer_dashboard/cart.html", {"cart_items": cart_items})


class AddressesPage(LoginRequiredMixin, View):
    def get(self, request):
        addresses = Address.objects.filter(user=request.user)
        return render(request, "customer_dashboard/addresses.html", {"addresses": addresses})


class NotificationsPage(LoginRequiredMixin, View):
    def get(self, request):
        notifications = Notification.objects.filter(customer=request.user).order_by('-created_at')
        return render(request, "customer_dashboard/notifications.html", {"notifications": notifications})


class SupportTicketsPage(LoginRequiredMixin, View):
    def get(self, request):
        tickets = SupportTicket.objects.filter(customer=request.user).order_by('-created_at')
        return render(request, "customer_dashboard/support_tickets.html", {"tickets": tickets})


class InvoicePage(LoginRequiredMixin, View):
    def get(self, request, order_id):
        try:
            order = Order.objects.get(pk=order_id, user=request.user)
        except Order.DoesNotExist:
            return render(request, "customer_dashboard/invoice_error.html", {"order_id": order_id})

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="invoice_{order_id}.pdf"'

        p = canvas.Canvas(response)
        p.setFont("Helvetica", 12)
        p.drawString(100, 800, f"Invoice for Order #{order.id}")
        p.drawString(100, 780, f"Date: {order.created_at.strftime('%Y-%m-%d')}")
        p.drawString(100, 760, f"Status: {order.status}")
        p.drawString(100, 740, "Items:")

        y = 720
        for item in order.orderitem_set.all():
            p.drawString(120, y, f"{item.product.title} x {item.quantity} @ {item.price} each")
            y -= 20

        p.drawString(100, y - 20, "Thank you for your purchase!")
        p.showPage()
        p.save()
        return response


class CustomerOrderHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class CustomerProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        })


class CustomerRecommendedProductsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Simplified recommendation: return most ordered products
        ordered_product_ids = OrderItem.objects.values_list('product_id', flat=True)
        popular_products = Product.objects.filter(id__in=ordered_product_ids).distinct()[:10]
        return Response({"recommended": [p.title for p in popular_products]})


class WishlistView(generics.ListCreateAPIView):
    serializer_class = WishlistItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WishlistItem.objects.filter(user=self.request.user)


class WishlistDetailView(generics.DestroyAPIView):
    serializer_class = WishlistItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return get_object_or_404(WishlistItem, user=self.request.user, pk=self.kwargs['pk'])


class CartView(generics.ListAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)


class OrderSummaryView(generics.ListAPIView):
    serializer_class = OrderSummarySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class AddressView(generics.ListCreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)


class AddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Address, user=self.request.user, pk=self.kwargs['pk'])


class SupportTicketListCreateView(generics.ListCreateAPIView):
    serializer_class = SupportTicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SupportTicket.objects.filter(customer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class TicketReplyListCreateView(generics.ListCreateAPIView):
    serializer_class = TicketReplySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TicketReply.objects.filter(ticket__customer=self.request.user)

    def perform_create(self, serializer):
        ticket_id = self.request.data.get('ticket')
        serializer.save(ticket_id=ticket_id, sender="customer")


class InvoiceDownloadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, order_id):
        order = Order.objects.get(pk=order_id, customer=request.user)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="invoice_{order_id}.pdf"'

        p = canvas.Canvas(response)
        p.setFont("Helvetica", 12)
        p.drawString(100, 800, f"Invoice for Order #{order.id}")
        p.drawString(100, 780, f"Date: {order.created_at.strftime('%Y-%m-%d')}")
        p.drawString(100, 760, f"Status: {order.status}")
        p.drawString(100, 740, f"Items:")

        y = 720
        for item in order.orderitem_set.all():
            p.drawString(120, y, f"{item.product.title} x {item.quantity} @ {item.price} each")
            y -= 20

        p.drawString(100, y - 20, "Thank you for your purchase!")
        p.showPage()
        p.save()
        return response


class AdminTicketReplyView(generics.CreateAPIView):
    serializer_class = TicketReplySerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        ticket_id = self.kwargs['ticket_id']
        ticket = SupportTicket.objects.get(id=ticket_id)
        serializer.save(ticket=ticket, sender='admin')


class UnreadNotificationsView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(customer=self.request.user, is_read=False)


class CustomerTicketListView(generics.ListAPIView):
    serializer_class = SupportTicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = SupportTicket.objects.filter(customer=self.request.user)
        status = self.request.query_params.get('status')
        if status in ['open', 'closed']:
            qs = qs.filter(status=status)
        return qs


class AdminReplyToTicketView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminOrSuperAdmin]

    def post(self, request, ticket_id):
        ticket = SupportTicket.objects.filter(id=ticket_id).first()
        if not ticket:
            return Response({'error': 'Ticket not found'}, status=404)

        reply = TicketReply.objects.create(
            ticket=ticket,
            sender='admin',
            message=request.data.get('message')
        )
        return Response(TicketReplySerializer(reply).data, status=201)


class NotificationListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(customer=self.request.user).order_by('-created_at')


class NotificationMarkReadView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    lookup_field = 'pk'

    def patch(self, request, *args, **kwargs):
        notification = self.get_object()
        if notification.customer != request.user:
            return Response({'error': 'Unauthorized'}, status=403)
        notification.is_read = True
        notification.save()
        return Response({'status': 'marked as read'})


class CustomerSupportTicketListCreateView(generics.ListCreateAPIView):
    serializer_class = SupportTicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        status_filter = self.request.query_params.get('status')
        queryset = SupportTicket.objects.filter(customer=self.request.user)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset
