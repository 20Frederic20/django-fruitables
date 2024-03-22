from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import JsonResponse
from products.cart import Cart
from django.views.generic import ListView, DetailView
from .models import Category, Product
# Create your views here.


class IndexView(View):
    template_name = "products/index.html"
    context_object_name = 'products'

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        categories = Category.objects.order_by('name')[:4]
        slug = request.GET.get('category')
        if slug:
            products = products.filter(category__slug=slug)
        context = {"categories": categories, "products": products[:12]}
        return render(request, self.template_name, context)


class ContactView(View):
    template_name = "products/contact.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class CartView(View):
    template_name = "products/cart.html"

    def get(self, request, *args, **kwargs):
        cart = request.session.get('session-key')
        products = []
        for product_id, product_data in cart.items():
            products.append(product_data)
        return render(request, self.template_name, context={'products': products})

    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, pk=product_id)
        cart.add(product=product)
        cart_quantity = cart.__len__()
        name = cart.cart[str(product_id)]['name']
        new_price = cart.cart[str(product_id)]['total']
        quantity = cart.cart[str(product_id)]['quantity']
        priceHT = cart.setPriceHT()
        return JsonResponse({'name': name, "cart_quantity": cart_quantity, "quantity": quantity, 'price': new_price, 'priceHT': priceHT})


class Error404View(View):
    template_name = "products/404.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class CheckoutView(View):
    template_name = "products/checkout.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class TestimonialView(View):
    template_name = "products/testimonial.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class ProductListView(ListView):
    template_name = "products/list_product.html"
    context_object_name = 'products'  # Le nom de la variable passée au template

    def get_queryset(self):
        # Récupérer tous les produits
        return Product.objects.all()[:9]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ajouter la liste de catégories au contexte
        context['categories'] = Category.objects.all()
        context['product_types'] = [(choice[0], choice[1])
                                    for choice in Product.TypeProduct.choices]
        return context


class ProductDetailView(DetailView):
    template_name = "products/detail_product.html"
    context_object_name = 'product'

    def get_queryset(self):
        # Récupérer tous les produits
        return Product.objects.filter(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ajouter la liste de catégories au contexte
        context['categories'] = Category.objects.all()
        return context
