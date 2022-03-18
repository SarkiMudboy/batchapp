from django.shortcuts import render, Http404
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponseRedirect
from django.forms.models import model_to_dict
from django.template.loader import render_to_string
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView, FormView

from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin, ProcessFormView

from django.views.generic.edit import FormMixin
from django.db import IntegrityError
from django.core import serializers
from products.models import Product
from datetime import date
from products.models import RawMaterial, Product, Specification
from bmr.mixins import AjaxFormMixin, serialize_model

from .forms import (ProductYieldForm, ProductSampleForm, QuantitySaleForm, 
	ReconPackMaterialForm, BatchReleaseForm)

from .models import *

import json


class ProductYieldView(ListView):
	template_name = "last_temp/product_recon.html"
	model = ProductYield
	context_object_name = 'yields'

	def get_queryset(self, *args, **kwargs):
		request = self.request
		pk = self.kwargs.get('pk2')
		batch = Batch.objects.get(pk=pk)
		query_set = ProductYield.objects.filter(batch=batch)
		if query_set is None:
			raise Http404('Batch info could not be found')
		return query_set

	def get_context_data(self, **kwargs):
		product = Product.objects.get(pk=self.kwargs.get('pk'))
		batch = Batch.objects.get(pk=self.kwargs.get('pk2'))
		context = super().get_context_data(**kwargs)
		context['records'] = self.request.session['batch_records']
		context['product'] = product
		context['batch'] = batch

		try:
			if ProductSamples.objects.filter(batch=batch) is not None:
				context.update({"product_samples": ProductSamples.objects.filter(batch=batch)})
		except ProductSamples.DoesNotExist:
			pass
		try:
			if ProductQuantitySale.objects.filter(batch=batch) is not None:
				form = QuantitySaleForm(instance=ProductQuantitySale.objects.filter(batch=batch))
				context.update({"quantity_sale_form": form})
		except ProductQuantitySale.DoesNotExist:
			pass

		try:
			if ProductReconPackMaterials.objects.filter(batch=batch) is not None:
				context.update({"recon_pack_materials": ProductReconPackMaterials.objects.filter(batch=batch)})
		except ProductReconPackMaterials.DoesNotExist:
			pass
		
		return context

class ProductYieldCreate(CreateView):
	template_name = "last_temp/product_yield_create.html"
	model = ProductYield
	form_class = ProductYieldForm

	def form_valid(self, form):
		batch = Batch.objects.get(pk=self.kwargs.get('pk2'))
		form.instance.batch = batch
		return super().form_valid(form)

	def get_success_url(self):
		product_id = self.kwargs.get('pk')
		return reverse_lazy('batches:product-reconciliation', kwargs={'pk': product_id, 'pk2': self.kwargs.get("pk2")})

	def get_context_data(self, **kwargs):
		product = Product.objects.get(pk=self.kwargs.get('pk'))
		batch = Batch.objects.get(pk=self.kwargs.get('pk2'))
		context = super().get_context_data(**kwargs)
		context['records'] = self.request.session['batch_records']
		context['product'] = product
		context['batch'] = batch
		return context

class YieldUpdateView(UpdateView): 
	template_name = "last_temp/product_yield_update.html"
	model = ProductYield
	form_class = ProductYieldForm
	context_object_name = 'yield'

	def get_object(self, *args, **kwargs):
		request = self.request
		pk = self.kwargs.get('pk3')
		instance = ProductYield.objects.get(pk=pk)
		if instance is None:
			raise Http404('Batch info could not be found')
		return instance

	def get_success_url(self):
		product_id = self.kwargs.get('pk')
		batch_id = self.kwargs.get('pk2')
		return reverse_lazy('batches:product-reconciliation', kwargs={'pk': product_id, 'pk2': batch_id})

class YieldDeleteView(DeleteView):
	model = Batch
	template_name = 'last_temp/yield_delete.html'

	def get_object(self, *args, **kwargs):
		request = self.request
		pk = self.kwargs.get('pk3')
		instance = ProductYield.objects.get(pk=pk)
		if instance is None:
			raise Http404('Batch info could not be found')
		return instance

	def get_success_url(self):
		product_id = self.kwargs.get('pk')
		batch_id = self.kwargs.get('pk2')
		return reverse_lazy('batches:product-reconciliation', kwargs={'pk': product_id, 'pk2': batch_id})


class ProductSampleCreate(CreateView):
	template_name = "last_temp/product_sample_create.html"
	model = ProductSamples
	form_class = ProductSampleForm

	def form_valid(self, form):
		batch = Batch.objects.get(pk=self.kwargs.get('pk2'))
		form.instance.batch = batch
		return super().form_valid(form)

	def get_success_url(self):
		product_id = self.kwargs.get('pk')
		return reverse_lazy('batches:product-reconciliation', kwargs={'pk': product_id, 'pk2': self.kwargs.get("pk2")})

	def get_context_data(self, **kwargs):
		product = Product.objects.get(pk=self.kwargs.get('pk'))
		batch = Batch.objects.get(pk=self.kwargs.get('pk2'))
		context = super().get_context_data(**kwargs)
		context['records'] = self.request.session['batch_records']
		context['product'] = product
		context['batch'] = batch
		return context

class SampleUpdateView(UpdateView): 
	template_name = "last_temp/product_sample_update.html"
	model = ProductSamples
	form_class = ProductSampleForm
	context_object_name = 'sample'

	def get_object(self, *args, **kwargs):
		request = self.request
		pk = self.kwargs.get('pk3')
		instance = ProductSamples.objects.get(pk=pk)
		if instance is None:
			raise Http404('Batch info could not be found')
		return instance

	def get_success_url(self):
		product_id = self.kwargs.get('pk')
		batch_id = self.kwargs.get('pk2')
		return reverse_lazy('batches:product-reconciliation', kwargs={'pk': product_id, 'pk2': batch_id})

class SampleDeleteView(DeleteView):
	model = ProductSamples
	template_name = 'last_temp/sample_delete.html'
	context_object_name = 'sample'

	def get_object(self, *args, **kwargs):
		request = self.request
		pk = self.kwargs.get('pk3')
		instance = ProductSamples.objects.get(pk=pk)
		if instance is None:
			raise Http404('Batch info could not be found')
		return instance

	def get_success_url(self):
		product_id = self.kwargs.get('pk')
		batch_id = self.kwargs.get('pk2')
		return reverse_lazy('batches:product-reconciliation', kwargs={'pk': product_id, 'pk2': batch_id})

class QuantitySampleView(AjaxFormMixin, FormView):

	model = ProductQuantitySale
	form_class = QuantitySaleForm
	message = ""
	
	def form_valid(self, form):

		if self.request.is_ajax:
			batch_obj = get_object_or_404(Batch, pk=self.kwargs.get('pk2'))
			try:
				if ProductQuantitySale.objects.get(batch=batch_obj) is not None:
					form = QuantitySaleForm(self.request.POST, instance=ProductQuantitySale.objects.get(batch=batch_obj))
			except ProductQuantitySale.DoesNotExist:
				form.instance.batch = batch_obj

			try:
				form.save()
				message = "Sample has been added!"
			except IntegrityError:
				message = "Sample already exists!"

			data = {
				'message': message
			}

			return JsonResponse(data)

		else:
			return super(AjaxFormMixin, self).form_valid(form)

class ReconPackMaterialCreate(CreateView):
	template_name = "last_temp/recon_pack_create.html"
	model = ProductReconPackMaterials
	form_class = ReconPackMaterialForm

	def form_valid(self, form):
		batch = Batch.objects.get(pk=self.kwargs.get('pk2'))
		form.instance.batch = batch
		return super().form_valid(form)

	def get_success_url(self):
		product_id = self.kwargs.get('pk')
		return reverse_lazy('batches:product-reconciliation', kwargs={'pk': product_id, 'pk2': self.kwargs.get("pk2")})

	def get_context_data(self, **kwargs):
		product = Product.objects.get(pk=self.kwargs.get('pk'))
		batch = Batch.objects.get(pk=self.kwargs.get('pk2'))
		context = super().get_context_data(**kwargs)
		context['records'] = self.request.session['batch_records']
		context['product'] = product
		context['batch'] = batch
		return context

class ReconPackMaterialUpdate(UpdateView): 
	template_name = "last_temp/recon_pack_update.html"
	model = ProductReconPackMaterials
	form_class = ReconPackMaterialForm
	context_object_name = 'packaging_material'

	def get_object(self, *args, **kwargs):
		request = self.request
		pk = self.kwargs.get('pk3')
		instance = ProductReconPackMaterials.objects.get(pk=pk)
		if instance is None:
			raise Http404('Batch info could not be found')
		return instance

	def get_success_url(self):
		product_id = self.kwargs.get('pk')
		batch_id = self.kwargs.get('pk2')
		return reverse_lazy('batches:product-reconciliation', kwargs={'pk': product_id, 'pk2': batch_id})

class ReconPackMaterialDelete(DeleteView):
	model = ProductReconPackMaterials
	template_name = 'last_temp/recon_pack_delete.html'
	context_object_name = 'packaging_material'

	def get_object(self, *args, **kwargs):
		request = self.request
		pk = self.kwargs.get('pk3')
		instance = ProductReconPackMaterials.objects.get(pk=pk)
		if instance is None:
			raise Http404('Batch info could not be found')
		return instance

	def get_success_url(self):
		product_id = self.kwargs.get('pk')
		batch_id = self.kwargs.get('pk2')
		return reverse_lazy('batches:product-reconciliation', kwargs={'pk': product_id, 'pk2': batch_id})


class BatchReleaseView(ListView):
	template_name = "last_temp/batch_release.html"
	model = ReleaseProfile
	context_object_name = 'profiles'

	def get_queryset(self, *args, **kwargs):
		request = self.request
		pk = self.kwargs.get('pk2')
		batch = Batch.objects.get(pk=pk)
		query_set = ReleaseProfile.objects.filter(batch=batch)
		if query_set is None:
			raise Http404('Batch info could not be found')
		return query_set

	def get_context_data(self, **kwargs):
		product = Product.objects.get(pk=self.kwargs.get('pk'))
		batch = Batch.objects.get(pk=self.kwargs.get('pk2'))
		context = super().get_context_data(**kwargs)
		context['records'] = self.request.session['batch_records']
		context['product'] = product
		context['batch'] = batch
		return context

class BatchReleaseCreate(CreateView):
	template_name = "last_temp/release_profile_create.html"
	model = ReleaseProfile
	form_class = BatchReleaseForm

	def form_valid(self, form):
		batch = Batch.objects.get(pk=self.kwargs.get('pk2'))
		form.instance.batch = batch
		return super().form_valid(form)

	def get_success_url(self):
		product_id = self.kwargs.get('pk')
		return reverse_lazy('batches:batch-release', kwargs={'pk': product_id, 'pk2': self.kwargs.get("pk2")})

	def get_context_data(self, **kwargs):
		product = Product.objects.get(pk=self.kwargs.get('pk'))
		batch = Batch.objects.get(pk=self.kwargs.get('pk2'))
		context = super().get_context_data(**kwargs)
		context['records'] = self.request.session['batch_records']
		context['product'] = product
		context['batch'] = batch
		return context

class BatchReleaseUpdate(UpdateView): 
	template_name = "last_temp/batch_release_update.html"
	model = ReleaseProfile
	form_class = BatchReleaseForm
	context_object_name = 'profile'

	def get_object(self, *args, **kwargs):
		request = self.request
		pk = self.kwargs.get('pk3')
		instance = ReleaseProfile.objects.get(pk=pk)
		if instance is None:
			raise Http404('Batch info could not be found')
		return instance

	def get_success_url(self):
		product_id = self.kwargs.get('pk')
		batch_id = self.kwargs.get('pk2')
		return reverse_lazy('batches:batch-release', kwargs={'pk': product_id, 'pk2': batch_id})

class BatchReleaseDelete(DeleteView):
	model = ReleaseProfile
	template_name = 'last_temp/batch_release_delete.html'
	context_object_name = 'profile'

	def get_object(self, *args, **kwargs):
		request = self.request
		pk = self.kwargs.get('pk3')
		instance = ReleaseProfile.objects.get(pk=pk)
		if instance is None:
			raise Http404('Batch info could not be found')
		return instance

	def get_success_url(self):
		product_id = self.kwargs.get('pk')
		batch_id = self.kwargs.get('pk2')
		return reverse_lazy('batches:batch-release', kwargs={'pk': product_id, 'pk2': batch_id})
