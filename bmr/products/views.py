from django.shortcuts import render, redirect, reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.messages import get_messages
from .models import Product, Equipment, RawMaterial, Specification, Test, ManufacturingProcess
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.shortcuts import get_object_or_404, Http404
from django.http import JsonResponse, HttpResponseRedirect
from django.core import serializers
from django.urls import reverse_lazy
from .forms import (
    ProductUpdateForm, ProductCreateForm, EquipmentCreateForm, 
    EquipmentUpdateForm, RawmaterialCreateForm, RawmaterialUpdateForm,
    SpecificationUpdateForm, SpecificationCreateForm, TestUpdateForm, TestCreateForm,
)
import json

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

class ProductUpdateView(SuccessMessageMixin, UpdateView):
    template_name = 'products/product_update.html'
    model = Product
    form_class = ProductUpdateForm
    success_message = '%(product_name)s was updated successfully'

class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('products:list')

class ProductCreateView(SuccessMessageMixin, CreateView):
    template_name = 'products/product_create_form.html'
    model = Product
    form_class = ProductCreateForm
    success_url = reverse_lazy('products:list')
    success_message = '%(product_name)s was created successfully'

# equipments

def equipment_list(request):
    equipments = Equipment.objects.all()
    form = EquipmentCreateForm
    # eq_instance = Equipment.objects.get(pk=pk)
    # update_form = EquimentUpdateForm(request.POST, instance=eq_instance)
    context = {
        'equipments': equipments,
        'form': form,
        'update_form': update_form
    }
    return render(request, 'equipments/equipment_list.html', context=context)

def equipment_modal(request, id):
    instance = get_object_or_404(Equipment, id=pk)
    context={
        'instance': instance
    }
    return render(request, 'update_modal.html', context)

def postEquipment(request):

    # validates request.
    if request.is_ajax and request.method == 'POST':
        # get the form data
        form = EquipmentCreateForm(request.POST)
        if form.is_valid():
            instance = form.save()

            # add success message
            equipment = form.cleaned_data['name']
            messages.add_message(request, messages.SUCCESS, f'{equipment} was created successfully')
            
            django_messages = []
            for message in messages.get_messages(request):
                django_messages.append({
                    "level": message.level,
                    "message": message.message,
                    "extra_tags": message.tags,
            })

            data = {}
            data['messages'] = django_messages

            # serialize new equipment object in json.
            ser_instance = serializers.serialize('json', [instance,])
            # send to the client side
            return JsonResponse({'instance': ser_instance, 'message': data}, status=200)
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

class EquipmentCreateView(SuccessMessageMixin, CreateView):
    template_name = 'equipments/equipment_create_form.html'
    model = Equipment
    form_class = EquipmentCreateForm
    success_url = reverse_lazy('products:equipments')
    success_message = '%(name)s was created successfully'

def equipment_update(request):

    if request_is_ajax and request.method == 'POST':
        if form.is_valid:
            form = EquipmentUpdateForm(request.POST)
            instance = form.save()

            equipment = form.cleaned_data['name']
            messages.add_message(request, SUCCESS, f'{equipment} have been updated')

            django_messages = []
            for message in messages.get_messages(request):
                django_messages.append({
                    'level': message.level,
                    'messages': message.message,
                    'extra_tags': message.tags
                })

            data = {}
            data['messages'] = django_messages

            ser_instance = serializers.serialize('json', [instance,])
            return JsonResponse({'instance': ser_instance, 'message' : data}, status=200)
        else:
            return JsonResponse({'error': form.errors}, status=400)

    else:
        return JsonResponse({'error': ''}, status=400)

class EquipmentUpdateView(SuccessMessageMixin, UpdateView):
    template_name = 'equipments/equipment_update.html'
    model = Equipment
    form_class = EquipmentUpdateForm
    success_message = '%(name)s was updated successfully'

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
            # add success message
            raw_material = form.cleaned_data['name']
            messages.add_message(request, messages.SUCCESS, f'{raw_material} was created successfully')
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

class RawmaterialUpdateView(SuccessMessageMixin, UpdateView):
    template_name = 'raw_materials/rawmaterial_update.html'
    model = RawMaterial
    form_class = RawmaterialUpdateForm
    success_message = '%(name)s was updated successfully'

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

class ProductSpecificationUpdateView(SuccessMessageMixin, UpdateView):
    template_name = 'specifications/product_specification_update.html'
    model = Specification
    form_class = SpecificationUpdateForm
    success_message = '%(test)s was updated successfully'

    def get_object(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk2')
        instance = Specification.objects.get(pk=pk)
        if instance is None:
            raise Http404('Specification could not be found')
        return instance

    def get_success_url(self):
        product_id=self.kwargs['pk']
        return reverse_lazy('products:specs', kwargs={'pk': product_id})


class ProductSpecificationDeleteView(DeleteView):
    model = Specification
    template_name = 'specifications/product_specification_confirm_delete.html'

    def get_object(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk2')
        instance = Specification.objects.get(pk=pk)
        if instance is None:
            raise Http404('Specification could not be found')
        return instance

    def get_success_url(self):
        product_id=self.kwargs['pk']
        return reverse_lazy('products:specs', kwargs={'pk': product_id})


class ProductSpecificationCreateView(SuccessMessageMixin, CreateView):
    template_name = 'specifications/product_specification_create_form.html'
    model = Specification
    form_class = SpecificationCreateForm
    success_message = '%(test)s was created successfully'

    def get_success_url(self):
        product_id=self.kwargs['pk']
        return reverse_lazy('products:specs', kwargs={'pk': product_id})

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.get(pk=pk)
        return context

# Tests

class TestView(ListView):
    template_name = 'product_tests/test_list.html'
    model = Test
    context_object_name = 'tests'

class TestCreateView(SuccessMessageMixin, CreateView):
    template_name = 'products_tests/test_create_form.html'
    model = Test
    form_class = TestCreateForm
    success_url = reverse_lazy('products:tests')
    success_message = '%(name)s was created successfully'

class TestDetailView(DetailView):
    template_name = 'products_tests/test_detail.html'
    context_object_name = 'test'

    def get_object(self, *args, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        instance = Test.objects.get(pk=pk)
        if instance is None:
            raise Http404('Test could not be found')
        return instance

class TestUpdateView(SuccessMessageMixin, UpdateView):
    template_name = 'products_tests/test_update.html'
    model = Test
    form_class = TestUpdateForm
    success_message = '%(name)s was updated successfully'

class TestDeleteView(DeleteView):
    template_name = 'products_tests/test_confirm_delete.html'
    model = Test
    success_url = reverse_lazy('products:tests')

