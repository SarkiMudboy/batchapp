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
from django.template.loader import render_to_string
from .forms import (
    ProductUpdateForm, ProductCreateForm, EquipmentCreateForm, 
    EquipmentUpdateForm, RawmaterialCreateForm, RawmaterialUpdateForm,
    SpecificationUpdateForm, SpecificationCreateForm, TestUpdateForm, TestCreateForm,
    ProcessCreateForm, ProcessUpdateForm,
)
import json

# Create your views here.

def homepage(request):
    return render(request, "home/home_page.html")

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
    context = {
        'equipments': equipments,
        'create_form': form,
    }
    return render(request, 'equipments/equipment_list.html', context=context)

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
            error_list = list()

            for field in form:
                for error in field.errors:
                    error_list.append(error)
                    
            # some form errors occured.
            return JsonResponse({"errors": error_list}, status=400)
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

# Update
def equipment_update(request, pk):
    equipment = Equipment.objects.get(pk=pk)
    data = {}
    if request.is_ajax and request.method == "POST":
        form = EquipmentUpdateForm(request.POST, instance=equipment)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            equipments = Equipment.objects.all()
            data['html_equipments_list'] = render_to_string('equipments/equipment_list.html', {'equipments': equipments}, request=request)
            messages.add_message(request, messages.SUCCESS, f'{equipment} was updated successfully')
            
            django_messages = []
            for message in messages.get_messages(request):
                django_messages.append({
                    "level": message.level,
                    "message": message.message,
                    "extra_tags": message.tags,
            })
            data['messages'] = django_messages
        else:
            data['form_is_valid'] = False
    else:
        form = EquipmentUpdateForm(instance=equipment)

    context = {'form': form, 'equipment': equipment}

    data['html_form'] = render_to_string('equipments/equipment_update.html', context, request=request)

    return JsonResponse(data)
    

def equipment_delete(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    data = dict()
    data['delete'] = True
    if request.method == 'POST':
        equipment.delete()
        data['form_is_valid'] = True
        equipments = Equipment.objects.all()
        messages.add_message(request, messages.ERROR, f'{equipment} has been deleted')
            
        django_messages = []
        for message in messages.get_messages(request):
            django_messages.append({
                "level": message.level,
                "message": message.message,
                "extra_tags": message.tags,
            })
            data['messages'] = django_messages
        data['html_equipments_list'] = render_to_string('equipments/equipment_list.html', {'equipments': equipments}, request=request)
    else:
        context = {'equipment': equipment}
        data['html_delete'] = render_to_string('equipments/equipment_confirm_delete.html', context, request=request)

    return JsonResponse(data)

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
    return render(request, 'raw_materials/raw_material_create_form.html', context)

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

    def form_valid(self, form):
        form.instance.product = Product.objects.get(pk=self.kwargs.get('pk'))
        return super().form_valid(form)

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
        product_id = self.kwargs['pk']
        return reverse_lazy('products:specs', kwargs={'pk': product_id})


class ProductSpecificationCreateView(SuccessMessageMixin, CreateView):
    template_name = 'specifications/product_specification_create_form.html'
    model = Specification
    form_class = SpecificationCreateForm
    success_message = '%(test)s was created successfully'

    def get_success_url(self):
        product_id=self.kwargs['pk']
        return reverse_lazy('products:specs', kwargs={'pk': product_id})

    def form_valid(self, form):
        form.instance.product = Product.objects.get(pk=self.kwargs.get('pk'))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.get(pk=pk)
        return context

# Tests

# convert this view to a function and merge with create view 

def tests(request):
    data = dict()
    if request.is_ajax and request.method == 'POST':
        form = TestCreateForm(request.POST)
        if form.is_valid():
            form.save()
            data['created'] = True
            new_tests = Test.objects.all()
            data['html_test_list'] = render_to_string('product_tests/test_list.html', {'tests': new_tests}, request=request)
            new_test = form.cleaned_data['name']
            messages.add_message(request, messages.SUCCESS, f'{new_test} added!')
            
            django_messages = []
            for message in messages.get_messages(request):
                django_messages.append({
                    "level": message.level,
                    "message": message.message,
                    "extra_tags": message.tags,
            })
            data['messages'] = django_messages
            return JsonResponse(data)
    else:
        tests = Test.objects.all()
        form = TestCreateForm    
        context = {
            'tests': tests,
            'create_form': form,
        }
        return render(request, 'product_tests/test_list.html', context=context)

def test_update(request, pk):
    test = Test.objects.get(pk=pk)
    data = {}
    if request.is_ajax and request.method == "POST":
        form = TestUpdateForm(request.POST, instance=test)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            tests = Test.objects.all()
            data['html_test_list'] = render_to_string('product_tests/test_list.html', {'tests': tests}, request=request)
            messages.add_message(request, messages.SUCCESS, f'{test} has a new name!')
            
            django_messages = []
            for message in messages.get_messages(request):
                django_messages.append({
                    "level": message.level,
                    "message": message.message,
                    "extra_tags": message.tags,
            })
            data['messages'] = django_messages
        else:
            data['form_is_valid'] = False
    else:
        form = TestUpdateForm(instance=test)

    context = {'form': form, 'test': test}

    data['html_form'] = render_to_string('product_tests/test_update.html', context, request=request)

    return JsonResponse(data)

# test this view
def test_delete(request, pk):
    test = get_object_or_404(Test, pk=pk)
    data = dict()
    data['delete'] = True
    if request.method == 'POST':
        test.delete()
        data['form_is_valid'] = True
        tests = Test.objects.all()
        messages.add_message(request, messages.ERROR, f'{test} has been deleted')
            
        django_messages = []
        for message in messages.get_messages(request):
            django_messages.append({
                "level": message.level,
                "message": message.message,
                "extra_tags": message.tags,
            })
            data['messages'] = django_messages
        data['html_tests_list'] = render_to_string('product_tests/test_list.html', {'tests': tests}, request=request)
    else:
        context = {'test': test}
        data['html_delete'] = render_to_string('product_tests/test_confirm_delete.html', context, request=request)

    return JsonResponse(data)

# Proccess

def manufacturing_process(request, pk):
    product = Product.objects.get(pk=pk)
    processes = ManufacturingProcess.objects.filter(product=product)

    context = {
        'processes': processes,
        'product': product

    }
    return render(request, 'process/process_list.html', context)

class ProcessCreateView(SuccessMessageMixin, CreateView):
    template_name = 'process/process_create.html'
    model = ManufacturingProcess
    form_class = ProcessCreateForm
    success_message = '%(step)s created!'

    def get_success_url(self):
        product_id=self.kwargs['pk']
        return reverse_lazy('products:process', kwargs={'pk': product_id})

    def get_form_kwargs(self):
        kw = super(ProcessCreateView, self).get_form_kwargs()
        kw['request_kwargs'] = self.kwargs
        return kw

    def form_valid(self, form):
        form.instance.product = Product.objects.get(pk=self.kwargs.get('pk'))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.get(pk=pk)
        return context

class ProcessUpdateView(SuccessMessageMixin, UpdateView):
    template_name = 'process/process_update.html'
    model = ManufacturingProcess
    form_class = ProcessUpdateForm

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk2')
        instance = ManufacturingProcess.objects.get(pk=pk)
        if instance is None:
            raise Http404('Process not found!')
        return instance

    def get_form_kwargs(self):
        kw = super(ProcessUpdateView, self).get_form_kwargs()
        kw['request_kwargs'] = self.kwargs
        return kw

    def form_valid(self, form):
        form.instance.product = Product.objects.get(pk=self.kwargs.get('pk'))
        step = form.instance.step
        messages.success(self.request, f'{step} updated!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.get(pk=pk)
        return context

    def get_success_url(self):
        product_id = self.kwargs.get('pk')
        return reverse_lazy('products:process', kwargs={'pk': product_id})

class ProcessDeleteView(SuccessMessageMixin, DeleteView):
    template_name = 'process/process_confirm_delete.html'
    model = ManufacturingProcess
    success_message = '%(step)s deleted!'

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk2')
        instance = ManufacturingProcess.objects.get(pk=pk)
        if instance is None:
            raise Http404('Process not found!')
        return instance
    
    def get_success_url(self):
        product_id = self.kwargs.get('pk')
        return reverse_lazy('products:process', kwargs={'pk': product_id})
