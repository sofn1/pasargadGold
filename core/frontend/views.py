from django.views.generic import TemplateView
from django.shortcuts import redirect, render, get_object_or_404
from news.models.news import News
from blogs.models.blog import Blog
from banners.models import Banner
from heroes.models import Hero
from products.models.product import Product
from products.models.brand import Brand
from categories.services import ProductCategoryService


def home(request):
    category_service = ProductCategoryService()
    categories = category_service.get_active_categories_by_parent()

    return render(request, "home.html", {
        "hero": Hero.objects.filter(is_active=True).last(),
        "top_banners": Banner.objects.filter(is_active=True, position="top").order_by("priority"),
        "middle_banner": Banner.objects.filter(is_active=True, position="middle").last(),
        "bottom_banners": Banner.objects.filter(is_active=True, position="bottom").order_by("priority"),
        "categories": categories,
        "featured_products": Product.objects.filter(featured=True)[:8],
        "brands": Brand.objects.all(),
    })


def profile(request):
    return render(request, "profile.html")


def cart(request):
    return render(request, "cart.html")


def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    # Here you'd add logic to store product in session or user's cart
    # For now just print a debug message or redirect
    print(f"🛒 Adding product {product.name} to cart.")
    return redirect("cart")


def checkout(request):
    return render(request, "checkout.html")


def login_view(request):
    return render(request, "login.html")


def register(request):
    return render(request, "register.html")


def blog_list(request):
    return render(request, "blog_list.html", {"blogs": []})


def blog_detail(request, id):
    blog = get_object_or_404(Blog, id=id)
    return render(request, "blog_detail.html", {"blog": blog})


def news_list(request):
    return render(request, "news_list.html", {"news_items": []})


def news_detail(request, id):
    news_item = get_object_or_404(News, id=id)
    return render(request, "news_detail.html", {"news": news_item})


def notifications(request):
    return render(request, "notifications.html", {"notifications": []})


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, "product_detail.html", {"product": product})


def product_list(request):
    return render(request, "product_detail.html", {"products": []})


class CustomerRegisterPage(TemplateView):
    template_name = 'register/customer.html'


class SellerRegisterPage(TemplateView):
    template_name = 'register/seller.html'


class WriterRegisterPage(TemplateView):
    template_name = 'register/writer.html'
