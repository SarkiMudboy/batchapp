from django.shortcuts import render, redirect, reverse
from .models import Product, Equipment, RawMaterial, Specification
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.shortcuts import get_object_or_404, Http404
from django.http import JsonResponse, HttpResponseRedirect
from django.core import serializers
from django.urls import reverse_lazy
from .forms import (
    ProductUpdateForm, ProductCreateForm, EquipmentCreateForm, 
    EquipmentUpdateForm, RawmaterialCreateForm, RawmaterialUpdateForm,
    SpecificationUpdateForm, SpecificationCreateForm
)

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

# equipments

def equipment_list(request):
    equipments = Equipment.objects.all()
    form = EquipmentCreateForm
    context = {
        'equipments': equipments,
        'form': form
    }
    return render(request, 'equipments/equipment_list.html', context=context)

def postEquipment(request):

    # validates request.
    if request.is_ajax and request.method == 'POST':
        # get the form data
        form = EquipmentCreateForm(request.POST)
        if form.is_valid():
            instance = form.save()
            # serialize new equipment object in json.
            ser_instance = serializers.serialize('json', [instance, ])
            # send to the client side
            return JsonResponse({'instance': ser_instance}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"error": form.errors}, status=400)
    # some error occured.
    return JsonResponse({'error': ''}, status=400)


class EquipmentListView(ListView):
    template_name = 'equipments/equipment_list.html'
    model = Equipment
    form_class = EquipmentCreateForm
    context_object_name = 'equipments'

class EquipmentCreateView(CreateView):
    template_name = 'equipments/equipment_create_form.html'
    model = Equipment
    form_class = EquipmentCreateForm
    success_url = reverse_lazy('products:equipments')


class EquipmentDetailView(DetailView):
    template_name = 'equipments/equipment_detail.html'
    context_object_name = 'equipment'

    def get_object(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        instance = Equipment.objects.get(pk=pk)
        if instance is None:
            raise Http404('Equipment could not be found')
        return instance

class EquipmentUpdateView(UpdateView):
    template_name = 'equipments/equipment_update.html'
    model = Equipment
    form_class = EquipmentUpdateForm

class EquipmentDeleteView(DeleteView):
    template_name = 'equipments/equipment_confirm_delete.html'
    model = Equipment
    success_url = reverse_lazy('products:equipments')

# raw materials

def raw_materials(request):
    raw_materials = RawMaterial.objects.all()
    context = {
        'raw_materials': raw_materials,
    }
    return render(request, 'raw_materials/raw_materials.html', context=context)

def create_raw_material(request):
    # instantiate an empty form
    form = None
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RawmaterialCreateForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # proccess and save the cleaned data to the database
            instance = form.save()
            # redirect to a new URL:
            return redirect(reverse('products:raw-materials'))
    else:
        form = RawmaterialCreateForm

    context = {
        'form' : form
    }
    return render(request , 'raw_materials/raw_material_create_form.html', context)

class RawmaterialDetailView(DetailView):
    template_name = 'raw_materials/rawmaterial_detail.html'
    context_object_name = 'raw_material'

    def get_object(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        instance = RawMaterial.objects.get(pk=pk)
        if instance is None:
            raise Http404('Raw material could not be found')
        return instance

class RawmaterialUpdateView(UpdateView):
    template_name = 'raw_materials/rawmaterial_update.html'
    model = RawMaterial
    form_class = RawmaterialUpdateForm

class RawmaterialDeleteView(DeleteView):
    template_name = 'raw_materials/rawmaterial_confirm_delete.html'
    model = RawMaterial
    success_url = reverse_lazy('products:raw-materials')


# specs

class ProductSpecificationListView(ListView):
    template_name = 'specifications/product_specification_list.html'
    model = Specification
    context_object_name = 'specs'

    def get_queryset(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        product = Product.objects.get(pk=pk)
        queryset = Specification.objects.filter(product=product)
        if queryset is None:
            raise Http404('Specification could not be found')
        return queryset

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.get(pk=pk)
        return context

class ProductSpecificationDetailView(DetailView):
    template_name = 'specifications/product_specification_detail.html'
    context_object_name = 'specs'

    def get_object(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk2')
        instance = Specification.objects.get(pk=pk)
        if instance is None:
            raise Http404('Specification could not be found')
        return instance

class ProductSpecificationUpdateView(UpdateView):
    template_name = 'specifications/product_specification_update.html'
    model = Specification
    form_class = SpecificationUpdateForm

    def get(self, request, *args, **kwargs):
        # pk1 = kwargs.get('pk', None)
        pk = kwargs.get('pk2', None) 
        return super(ProductSpecificationUpdateView, self).get(request, *args, **kwargs)

class ProductSpecificationDeleteView(DeleteView):
    model = Specification
    success_url = reverse_lazy('products:specs')

    def get(self, *args, **kwargs):
        # pk1 = kwargs.get('pk1', None)
        pk = kwargs.get('pk2', None)
        return super(ProductSpecificationDeleteView, self).get(*args, **kwargs)

class ProductSpecificationCreateView(CreateView):
    template_name = 'specifications/product_specification_create_form.html'
    model = Specification
    form_class = SpecificationCreateForm
    success_url = reverse_lazy('products:specs')

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.get(pk=pk)
        return context