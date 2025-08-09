from django.views import View
from django.shortcuts import render
from reportlab.pdfgen import canvas
from orders.models import OrderItem
from django.http import HttpResponse
from orders.models import Order, CartItem
from products.models.product import Product
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import WishlistItem, Address, Notification, SupportTicket
from django.contrib.auth.decorators import login_required, user_passes_test


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
        customer = request.user.customer
        addresses = Address.objects.filter(customer=customer)
        return render(request, "customer_dashboard/addresses.html", {"addresses": addresses})


class NotificationsPage(LoginRequiredMixin, View):
    def get(self, request):
        customer = request.user.customer  # ✅ Convert User to Customer
        notifications = Notification.objects.filter(customer=customer).order_by('-created_at')
        return render(request, "customer_dashboard/notifications.html", {"notifications": notifications})


class SupportTicketsPage(LoginRequiredMixin, View):
    def get(self, request):
        customer = request.user.customer  # ✅ fix
        tickets = SupportTicket.objects.filter(customer=customer).order_by('-created_at')
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

