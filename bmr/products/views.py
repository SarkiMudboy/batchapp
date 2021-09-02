from django.shortcuts import render
from .models import Product
from django.views.generic import ListView, DetailView

# Create your views here.

def product_list(request):

    products = Product.objects.all()
    context = {
        'products': products 
    }

    return render(request, 'products/product_list.html', context)

class ProductListView(ListView):
    template_name = 'products/product_list.html'
    model = Product
    context_object_name = 'products'

class ProductDetailView(DetailView):
    template_name = 'products/product_detail.html'
    context_object_name = 'object'

    def get_queryset(self):
        self.product = get_object_or_404(Product, pk=self.id)
        return Product.objects.get(product_name=self.product)
