from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView
from .models import Category, Product
# Create your views here.


class IndexView(View):
    template_name = "products/index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class ProductListView(ListView):
    template_name = "products/list_product.html"
    context_object_name = 'products'  # Le nom de la variable passée au template

    def get_queryset(self):
        # Récupérer tous les produits
        return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ajouter la liste de catégories au contexte
        context['categories'] = Category.objects.all()
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
