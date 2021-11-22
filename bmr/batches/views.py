from django.shortcuts import render, Http404
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView, FormView
from django.views.generic.edit import FormMixin
from django.db import IntegrityError
from products.models import Product
from datetime import date
from .models import *
from .forms import (BatchCreateForm, BatchUpdateForm, BatchRecordsCheckForm, BatchInfoForm, GuideForm,
	EquipmentCheckListForm,)

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

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		form = self.get_form()
		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)    

	def get_context_data(self, **kwargs):
		product = Product.objects.get(pk=self.kwargs.get('pk'))
		context = super().get_context_data(**kwargs)
		context['product'] = product
		context['form'] = self.get_form()
		return context

	def attach_views(self, view_list):
		return_list = list()
		for page_name in view_list:
			page_name = page_name.lower().replace(' ', '-')
			return_list.append("batches:" + page_name)
		return return_list

	def get_success_url(self):
		product_id = self.kwargs.get('pk')
		batch_id = self.kwargs.get('pk2')
		records = self.request.POST.getlist(key='batch_records')
		attached_views = self.attach_views(records)
		session_data = {d: attached_views[i] for i, d in enumerate(records)}
		self.request.session['batch_records'] = session_data  
		return reverse_lazy(attached_views[0], kwargs={'pk': product_id, 'pk2': batch_id})


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

# Batch Records

class BatchInfoView(SuccessMessageMixin, FormView):
	template_name = 'batch/batch_info.html'
	form_class = BatchInfoForm
	model = BatchInfoAuth
	success_message = ''
	is_created = False

	def get_form(self, form_class=form_class):
		"""
		Check to see if the Batch already has an Info Auth to return form populated with batch_instance
		if not return the basic form 
		"""
		try:
			info_auth = BatchInfoAuth.objects.get(batch=get_object_or_404(Batch, pk=self.kwargs.get('pk2')))
			self.is_created = True
			return form_class(instance=info_auth, **self.get_form_kwargs())
		except BatchInfoAuth.DoesNotExist:	
			return form_class(**self.get_form_kwargs())

	def form_valid(self, form):
		form.instance.batch = get_object_or_404(Batch, pk=self.kwargs.get('pk2'))
		try:
			form.save() 
		except IntegrityError:
			pass
		return super(BatchInfoView, self).form_valid(form)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['records'] = self.request.session['batch_records']
		context['batch'] = get_object_or_404(Batch, pk=self.kwargs.get('pk2'))
		context['product'] = get_object_or_404(Product, pk=self.kwargs.get('pk'))
		if self.is_created:
			context['batch_info_auth'] = BatchInfoAuth.objects.get(batch=get_object_or_404(Batch, pk=self.kwargs.get('pk2')))
		return context

	def get_success_url(self):
		product_id = self.kwargs.get('pk')
		batch_id = self.kwargs.get('pk2')
		return reverse_lazy('batches:batch-info', kwargs={'pk': product_id, 'pk2': batch_id})

class BatchInfoDelete(DeleteView):
	template_name = 'batch/batchinfoauth_confirm_delete.html'
	model = BatchInfoAuth
	context_object_name = 'batch_info'

	def get_object(self, *args, **kwargs):
		request = self.request
		pk = self.kwargs.get('pk3')
		instance = BatchInfoAuth.objects.get(pk=pk)
		if instance is None:
			raise Http404('Batch Info could not be found')
		return instance

	def get_success_url(self):
		product_id = self.kwargs['pk']
		batch_id = self.kwargs.get('pk2')
		return reverse_lazy('batches:batch-info', kwargs={'pk': product_id, 'pk2': batch_id})


class ProductInitiationView(DetailView):
	template_name = 'batch/product_init.html'
	model = Batch
	context_object_name = 'batch'

	def get_object(self, *args, **kwargs):
		request = self.request
		pk = self.kwargs.get('pk2')
		instance = Batch.objects.get(pk=pk)
		if instance is None:
			raise Http404('Batch could not be found')
		return instance

	def get_context_data(self, **kwargs):
		product = Product.objects.get(pk=self.kwargs.get('pk'))
		batch = Batch.objects.get(pk=self.kwargs.get('pk2'))
		context = super().get_context_data(**kwargs)
		context['records'] = self.request.session['batch_records']
		context['product'] = product
		context['batch'] = batch
		return context

class GuideView(FormView):
	template_name = 'batch/guide.html'
	form_class = GuideForm
	model = Guide
	is_created = False

	def get_form(self, form_class=form_class):
		"""
		Check to see if the Batch already has an Info Auth to return form populated with batch_instance
		if not return the basic form 
		"""
		try:
			guide = Guide.objects.get(batch=get_object_or_404(Batch, pk=self.kwargs.get('pk2')))
			self.is_created = True
			return form_class(instance=guide, **self.get_form_kwargs())
		except Guide.DoesNotExist:	
			return form_class(**self.get_form_kwargs())

	def form_valid(self, form):
		form.instance.batch = get_object_or_404(Batch, pk=self.kwargs.get('pk2'))
		try:
			form.save() 
		except IntegrityError:
			pass
		return super(GuideView, self).form_valid(form)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['records'] = self.request.session['batch_records']
		context['batch'] = get_object_or_404(Batch, pk=self.kwargs.get('pk2'))
		context['product'] = get_object_or_404(Product, pk=self.kwargs.get('pk'))
		if self.is_created:
			context['guide'] = Guide.objects.get(batch=get_object_or_404(Batch, pk=self.kwargs.get('pk2')))
		return context

	def get_success_url(self):
		product_id = self.kwargs.get('pk')
		batch_id = self.kwargs.get('pk2')
		return reverse_lazy('batches:guide', kwargs={'pk': product_id, 'pk2': batch_id})

class GuideDelete(DeleteView):
	template_name = 'batch/guide_confirm_delete.html'
	model = Guide
	context_object_name = 'guide'

	def get_object(self, *args, **kwargs):
		request = self.request
		pk = self.kwargs.get('pk3')
		instance = Guide.objects.get(pk=pk)
		if instance is None:
			raise Http404('Guide could not be found')
		return instance

	def get_success_url(self):
		product_id = self.kwargs['pk']
		batch_id = self.kwargs.get('pk2')
		return reverse_lazy('batches:guide', kwargs={'pk': product_id, 'pk2': batch_id})

class EquipmentCheckListView(FormView):
	template_name = 'batch/equipment_check_list.html'
	form_class = EquipmentCheckListForm
	model = EquipmentCheck
	is_created = False

	def get_form(self, form_class=form_class):
		"""
		Check to see if the its an update request else return empty form
		"""
		if "pk3" in self.kwargs:
			eq_check = get_object_or_404(EquipmentCheck, pk=self.kwargs.get('pk3'))
			self.is_created = True
			return form_class(instance=eq_check, **self.get_form_kwargs())
		else:
			try:
				equipment_check = EquipmentCheck.objects.filter(batch=get_object_or_404(Batch, pk=self.kwargs.get('pk2')))	
				self.is_created = True
			except EquipmentCheck.DoesNotExist:
				pass
			return form_class(**self.get_form_kwargs())

	def form_valid(self, form):
		form.instance.batch = get_object_or_404(Batch, pk=self.kwargs.get('pk2'))
		try:
			form.save()
		except IntegrityError:
			pass
		return super(EquipmentCheckListView, self).form_valid(form)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['records'] = self.request.session['batch_records']
		context['batch'] = get_object_or_404(Batch, pk=self.kwargs.get('pk2'))
		context['product'] = get_object_or_404(Product, pk=self.kwargs.get('pk'))
		if self.is_created:
			context['check_list'] = EquipmentCheck.objects.filter(batch=get_object_or_404(Batch, pk=self.kwargs.get('pk2')))
		return context

	def get_success_url(self):
		product_id = self.kwargs.get('pk')
		batch_id = self.kwargs.get('pk2')
		return reverse_lazy('batches:equipment-check-list', kwargs={'pk': product_id, 'pk2': batch_id})

class EQCheckListDelete(DeleteView):
	template_name = 'batch/equipmentchecklist_confirm_delete.html'
	model = EquipmentCheck
	context_object_name = 'check_list'

	def get_object(self, *args, **kwargs):
		request = self.request
		pk = self.kwargs.get('pk3')
		instance = EquipmentCheck.objects.get(pk=pk)
		if instance is None:
			raise Http404('Batch Info could not be found')
		return instance

	def get_success_url(self):
		product_id = self.kwargs['pk']
		batch_id = self.kwargs.get('pk2')
		return reverse_lazy('batches:equipment-check-list', kwargs={'pk': product_id, 'pk2': batch_id})

# class EquipmentClearanceView(FormView):
# 	template_name = 'batch/equipment_clearance.html'
# 	form_class = EquipmentClearanceForm
# 	second_form_class = EQclearAuthForm
# 	model = EquipmentClearance
# 	is_created = False

# 	def get_form(self, form_class=form_class):
# 		"""
# 		Check to see if the its an update request else return empty form
# 		"""
# 		if "pk3" in self.kwargs:
# 			eq_clear = get_object_or_404(EquipmentClearance, pk=self.kwargs.get('pk3'))
# 			self.is_created = True
# 			return form_class(instance=eq_clear, **self.get_form_kwargs())
# 		else:
# 			try:
# 				equipment_clear = EquipmentClearance.objects.filter(batch=get_object_or_404(Batch, pk=self.kwargs.get('pk2')))	
# 				self.is_created = True
# 			except EquipmentClearance.DoesNotExist:
# 				pass
# 			return form_class(**self.get_form_kwargs())

# 	def form_valid(self, form):
# 		form.instance.batch = get_object_or_404(Batch, pk=self.kwargs.get('pk2'))
# 		try:
# 			form.save()
# 		except IntegrityError:
# 			pass
# 		return super(EquipmentClearanceView, self).form_valid(form)

# 	def get_context_data(self, **kwargs):
# 		context = super().get_context_data(**kwargs)
# 		context['records'] = self.request.session['batch_records']
# 		context['batch'] = get_object_or_404(Batch, pk=self.kwargs.get('pk2'))
# 		context['product'] = get_object_or_404(Product, pk=self.kwargs.get('pk'))
# 		context['form2'] = self.second_form_class(request=self.request)
# 		if self.is_created:
# 			context['clearance'] = EquipmentClearance.objects.filter(batch=get_object_or_404(Batch, pk=self.kwargs.get('pk2')))
# 		return context

# 	def get_success_url(self):
# 		product_id = self.kwargs.get('pk')
# 		batch_id = self.kwargs.get('pk2')
# 		return reverse_lazy('batches:equipment-check-list', kwargs={'pk': product_id, 'pk2': batch_id})

# class EQClearanceDelete(DeleteView):
# 	template_name = 'batch/equipmentclearance_confirm_delete.html'
# 	model = EquipmentClearance
# 	context_object_name = 'clearance'

# 	def get_object(self, *args, **kwargs):
# 		request = self.request
# 		pk = self.kwargs.get('pk3')
# 		instance = EquipmentClearance.objects.get(pk=pk)
# 		if instance is None:
# 			raise Http404('Batch Info could not be found')
# 		return instance

# 	def get_success_url(self):
# 		product_id = self.kwargs['pk']
# 		batch_id = self.kwargs.get('pk2')
# 		return reverse_lazy('batches:equipment-check-list', kwargs={'pk': product_id, 'pk2': batch_id})

