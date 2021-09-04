from django.shortcuts import render
from .models import Product
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.shortcuts import get_object_or_404, Http404
from django.urls import reverse_lazy
from .forms import ProductUpdateForm, ProductCreateForm

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
    context_object_name = 'product'

    def get_object(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        instance = Product.objects.get(pk=pk)
        if instance is None:
            raise Http404('Product could not be found')
        return instance

class ProductUpdateView(UpdateView):
    template_name = 'products/product_update.html'
    model = Product
    form_class = ProductUpdateForm

class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('products:list')

class ProductCreateView(CreateView):
    template_name = 'products/product_create_form.html'
    model = Product
    form_class = ProductCreateForm
    success_url = reverse_lazy('products:list')
