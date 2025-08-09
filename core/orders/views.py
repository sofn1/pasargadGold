# orders/views.py
from django.conf import settings
from django.db import transaction
from django.contrib import messages
from products.models.product import Product
from .zarinpal_client import ZarinpalGateway
from .forms import CartItemForm, CheckoutForm
from .models import CartItem, Order, OrderItem
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View, FormView


class CartPage(LoginRequiredMixin, TemplateView):
    template_name = "orders/cart.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        items = CartItem.objects.select_related("product").filter(user=self.request.user)
        total_price = sum((ci.product.price or 0) * ci.quantity for ci in items)  # assumes Product.price
        ctx["items"] = items
        ctx["total_price"] = total_price
        ctx["add_form"] = CartItemForm()
        return ctx

    def post(self, request, *args, **kwargs):
        """
        Handle add/update actions from the cart page.
        If the (user, product) exists, increase quantity; else create.
        """
        form = CartItemForm(request.POST)
        if form.is_valid():
            product = get_object_or_404(Product, pk=form.cleaned_data["product"])
            qty = form.cleaned_data["quantity"]

            obj, created = CartItem.objects.get_or_create(user=request.user, product=product, defaults={"quantity": qty})
            if not created:
                obj.quantity += qty
                obj.save()

            messages.success(request, "آیتم به سبد اضافه شد.")
        else:
            messages.error(request, "ورودی نامعتبر است.")
        return redirect("orders_cart")


class CartItemRemoveView(LoginRequiredMixin, View):
    def post(self, request, pk):
        item = get_object_or_404(CartItem, pk=pk, user=request.user)
        item.delete()
        messages.info(request, "آیتم از سبد حذف شد.")
        return redirect("orders_cart")


class CheckoutPage(LoginRequiredMixin, FormView):
    """
    Creates an Order from current cart and redirects to Zarinpal.
    """
    template_name = "orders/checkout.html"
    form_class = CheckoutForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        items = CartItem.objects.select_related("product").filter(user=self.request.user)
        total_price = sum((ci.product.price or 0) * ci.quantity for ci in items)
        ctx["items"] = items
        ctx["total_price"] = total_price
        return ctx

    @transaction.atomic
    def form_valid(self, form):
        user = self.request.user
        cart_items = list(CartItem.objects.select_related("product").filter(user=user))
        if not cart_items:
            messages.error(self.request, "سبد خرید خالی است.")
            return redirect("orders_cart")

        total_price = sum((ci.product.price or 0) * ci.quantity for ci in cart_items)

        # Create order + items
        order = Order.objects.create(
            user=user,
            total_price=total_price,
            address=form.cleaned_data["address"],
            location=form.cleaned_data.get("location") or "",
            status="pending",
        )
        OrderItem.objects.bulk_create([
            OrderItem(order=order, product=ci.product, quantity=ci.quantity) for ci in cart_items
        ])

        # optionally clear cart
        CartItem.objects.filter(user=user).delete()

        # Start Zarinpal payment (redirect)
        gateway = ZarinpalGateway(
            merchant_id=getattr(settings, "ZARINPAL_MERCHANT_ID", "your-merchant-id"),
            sandbox=getattr(settings, "ZARINPAL_SANDBOX", True),
        )
        callback_url = getattr(settings, "ZARINPAL_CALLBACK", "")
        phone = getattr(user, "phone_number", "")
        result = gateway.request_payment(
            amount=order.total_price,
            description=f"Order #{order.id}",
            callback_url=callback_url,
            phone=phone,
        )

        if result.get("status") == 100:
            order.authority = result["authority"]
            order.save(update_fields=["authority"])
            return redirect(result["url"])

        messages.error(self.request, "خطا در اتصال به زرین‌پال.")
        return redirect("orders_cart")


class ZarinpalVerifyView(View):
    """
    Callback endpoint from Zarinpal (configured in settings.ZARINPAL_CALLBACK).
    It redirects to SUCCESS/FAIL URLs defined in settings.
    """
    def get(self, request):
        authority = request.GET.get("Authority")
        status_param = request.GET.get("Status")

        order = Order.objects.filter(authority=authority).first()
        if not order:
            messages.error(request, "سفارش پیدا نشد.")
            return redirect(getattr(settings, "ZARINPAL_FAIL_URL", "/"))

        gateway = ZarinpalGateway(
            merchant_id=getattr(settings, "ZARINPAL_MERCHANT_ID", "your-merchant-id"),
            sandbox=getattr(settings, "ZARINPAL_SANDBOX", True),
        )
        result = gateway.verify_payment(order.total_price, authority)

        if result.get("status") == 100:
            order.status = "paid"
            order.save(update_fields=["status"])
            return redirect(getattr(settings, "ZARINPAL_SUCCESS_URL", "/"))
        else:
            order.status = "failed"
            order.save(update_fields=["status"])
            return redirect(getattr(settings, "ZARINPAL_FAIL_URL", "/"))
