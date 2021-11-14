from django.shortcuts import render, Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.views.generic.edit import FormMixin
from products.models import Product
from .models import *
from .forms import BatchCreateForm, BatchUpdateForm, BatchRecordsCheckForm

# Create your views here.

class BatchProductListView(ListView):
	template_name = 'batches/batch_products.html'
	model = Product
	context_object_name = 'products'

class BatchListView(ListView):
	template_name = 'batches/batches.html'
	model = Batch
	context_object_name = 'batches'
	
	def get_queryset(self, *args, **kwargs):
		pk = self.kwargs.get('pk')
		product = Product.objects.get(pk=pk)
		queryset = Batch.objects.filter(product=product)
		if queryset is None:
			raise Http404('Batches not found!')
		return queryset	

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		product = Product.objects.get(pk=self.kwargs.get("pk"))
		context['product'] = product
		return context

class BatchCreateView(CreateView):
	template_name = 'batches/batch_create.html'
	model = Batch
	context_object_name = 'batch'
	form_class = BatchCreateForm

	def form_valid(self, form):
		product = Product.objects.get(pk=self.kwargs.get('pk'))
		form.instance.product = product
		return super().form_valid(form)

	def get_success_url(self):
		product_id = self.kwargs.get('pk')
		return reverse_lazy('batches:batches', kwargs={'pk': product_id})

	def get_context_data(self, **kwargs):
		product = Product.objects.get(pk=self.kwargs.get('pk'))
		context = super().get_context_data(**kwargs)
		context['product'] = product
		return context


class BatchDetailView(FormMixin, DetailView):
	template_name = 'batches/batch_detail.html'
	model = Batch
	context_object_name = 'batch'
	form_class = BatchRecordsCheckForm

	def get_object(self, *args, **kwargs):
		request = self.request
		pk = self.kwargs.get('pk2')
		instance = Batch.objects.get(pk=pk)
		if instance is None:
			raise Http404('Batch could not be found')
		return instance

	def get_context_data(self, **kwargs):
		product = Product.objects.get(pk=self.kwargs.get('pk'))
		context = super().get_context_data(**kwargs)
		context['product'] = product
		context['form'] = self.get_form()
		return context


class BatchUpdateView(UpdateView): 
	template_name = "batches/batch_update.html"
	model = Batch
	form_class = BatchUpdateForm
	context_object_name = 'batch'
	success_message = '%(batch_number)s was updated successfully'

	def get_object(self, *args, **kwargs):
		request = self.request
		pk = self.kwargs.get('pk2')
		instance = Batch.objects.get(pk=pk)
		if instance is None:
			raise Http404('Batch could not be found')
		return instance

	def form_valid(self, form):
		form.instance.product = Product.objects.get(pk=self.kwargs.get('pk'))
		return super().form_valid(form)

	def get_success_url(self):
		product_id = self.kwargs.get('pk')
		batch_id = self.kwargs.get('pk2')
		return reverse_lazy('batches:batch-pages', kwargs={'pk': product_id, 'pk2': batch_id})

class BatchDeleteView(DeleteView):
	model = Batch
	template_name = 'batches/batch_confirm_delete.html'

	def get_object(self, *args, **kwargs):
		request = self.request
		pk = self.kwargs.get('pk2')
		instance = Batch.objects.get(pk=pk)
		if instance is None:
			raise Http404('Batch could not be found')
		return instance

	def get_success_url(self):
		product_id = self.kwargs['pk']
		return reverse_lazy('batches:batches', kwargs={'pk': product_id})


