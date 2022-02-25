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
from django.views.generic.edit import FormMixin
from django.db import IntegrityError
from django.core import serializers
from products.models import Product
from datetime import date
from products.models import RawMaterial, Product, Specification
from .models import (Batch, RawMaterialBillAuth, BatchManufacturingProcess, RawMaterialCheckRecord,
	IndividualWeight, ControlRecords, CleaningProcess)
from .forms import (RawMaterialBillForm, ProcessForm, RawMaterialCheckForm, InProcessControlForm,
	CleaningProcessForm, IndividualWeightForm,)


class MasterFormulaView(ListView):
	template_name = 'batch/master_formula.html'
	model = RawMaterial
	context_object_name = 'materials'

	def get_queryset(self, *args, **kwargs):
		request = self.request
		pk = self.kwargs.get('pk')
		product = Product.objects.get(pk=pk)
		query_set = RawMaterial.objects.filter(product=product)
		if query_set is None:
			raise Http404('Raw material could not be found')
		return query_set

	def get_context_data(self, **kwargs):
		product = Product.objects.get(pk=self.kwargs.get('pk'))
		batch = Batch.objects.get(pk=self.kwargs.get('pk2'))
		context = super().get_context_data(**kwargs)
		context['records'] = self.request.session['batch_records']
		context['product'] = product
		context['batch'] = batch
		return context

class BillofRawMaterialView(FormView):
	template_name = 'batch/raw_material_bill.html'
	form_class = RawMaterialBillForm
	model = RawMaterialBillAuth
	is_created = False

	def get_form(self, form_class=form_class):
		"""
		Check to see if the its an update request else return empty form
		"""
		if "pk3" in self.kwargs:
			rw_bill = get_object_or_404(RawMaterialBillAuth, pk=self.kwargs.get('pk3'))
			self.is_created = True
			return form_class(instance=rw_bill, **self.get_form_kwargs())
		else:
			try:
				raw_materials = RawMaterialBillAuth.objects.filter(batch=get_object_or_404(Batch, pk=self.kwargs.get('pk2')))	
				self.is_created = True
			except RawMaterialBillAuth.DoesNotExist:
				pass
			return form_class(**self.get_form_kwargs())

	def form_valid(self, form):
		form.instance.batch = get_object_or_404(Batch, pk=self.kwargs.get('pk2'))

		try:
			form.save()
		except IntegrityError:
			pass
		return super(BillofRawMaterialView, self).form_valid(form)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['records'] = self.request.session['batch_records']
		context['batch'] = get_object_or_404(Batch, pk=self.kwargs.get('pk2'))
		context['product'] = get_object_or_404(Product, pk=self.kwargs.get('pk'))
		if self.is_created:
			context['bills'] = RawMaterialBillAuth.objects.filter(batch=get_object_or_404(Batch, pk=self.kwargs.get('pk2')))
		return context

	def get_success_url(self):
		product_id = self.kwargs.get('pk')
		batch_id = self.kwargs.get('pk2')
		return reverse_lazy('batches:bill-of-raw-materials', kwargs={'pk': product_id, 'pk2': batch_id})

@method_decorator(csrf_exempt, name="dispatch")
class RMBillDelete(DeleteView):
	template_name = 'batch/rawmaterialbillauth_confirm_delete.html'
	model = RawMaterialBillAuth
	context_object_name = 'bill'

	def get_object(self, *args, **kwargs):
		request = self.request
		pk = self.kwargs.get('pk3')
		instance = RawMaterialBillAuth.objects.get(pk=pk)
		if instance is None:
			raise Http404('Batch Info could not be found')
		return instance

	def get_success_url(self):
		product_id = self.kwargs['pk']
		batch_id = self.kwargs.get('pk2')
		return reverse_lazy('batches:bill-of-raw-materials', kwargs={'pk': product_id, 'pk2': batch_id})

class BatchManufacturingView(FormView):
	template_name = 'batch/batch_process.html'
	form_class = ProcessForm
	model = BatchManufacturingProcess
	is_created = False

	def get_form(self, form_class=form_class):
		"""
		Check to see if the its an update request else return empty form
		"""
		if "pk3" in self.kwargs:
			process = get_object_or_404(BatchManufacturingProcess, pk=self.kwargs.get('pk3'))
			self.is_created = True
			return form_class(instance=process, **self.get_form_kwargs())
		else:
			try:
				batch_process = BatchManufacturingProcess.objects.filter(batch=get_object_or_404(Batch, pk=self.kwargs.get('pk2')))	
				self.is_created = True
			except BatchManufacturingProcess.DoesNotExist:
				pass
			return form_class(**self.get_form_kwargs())

	def form_valid(self, form):
		form.instance.batch = get_object_or_404(Batch, pk=self.kwargs.get('pk2'))

		try:
			form.save()
		except IntegrityError:
			pass
		return super(BatchManufacturingView, self).form_valid(form)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['records'] = self.request.session['batch_records']
		context['batch'] = get_object_or_404(Batch, pk=self.kwargs.get('pk2'))
		context['product'] = get_object_or_404(Product, pk=self.kwargs.get('pk'))
		if self.is_created:
			context['processes'] = BatchManufacturingProcess.objects.filter(batch=get_object_or_404(Batch, pk=self.kwargs.get('pk2')))
		return context

	def get_success_url(self):
		product_id = self.kwargs.get('pk')
		batch_id = self.kwargs.get('pk2')
		return reverse_lazy('batches:process', kwargs={'pk': product_id, 'pk2': batch_id})

@method_decorator(csrf_exempt, name='dispatch')
class ProcessDelete(DeleteView):
	template_name = 'batch/batchmanufacturingprocess_confirm_delete.html'
	model = BatchManufacturingProcess
	context_object_name = 'process'

	def get_object(self, *args, **kwargs):
		request = self.request
		pk = self.kwargs.get('pk3')
		instance = BatchManufacturingProcess.objects.get(pk=pk)
		if instance is None:
			raise Http404('Batch Info could not be found')
		return instance

	def get_success_url(self):
		product_id = self.kwargs['pk']
		batch_id = self.kwargs.get('pk2')
		return reverse_lazy('batches:process', kwargs={'pk': product_id, 'pk2': batch_id})


class RawMaterialCheckView(FormView):
	template_name = 'batch/raw_material_check.html'
	form_class = RawMaterialCheckForm
	model = RawMaterialCheckRecord
	is_created = False

	def get_form(self, form_class=form_class):
		"""
		Check to see if the its an update request else return empty form
		"""
		if "pk3" in self.kwargs:
			rw_check = get_object_or_404(RawMaterialCheckRecord, pk=self.kwargs.get('pk3'))
			self.is_created = True
			return form_class(instance=rw_check, **self.get_form_kwargs())
		else:
			try:
				raw_materials_check = RawMaterialCheckRecord.objects.filter(batch=get_object_or_404(Batch, pk=self.kwargs.get('pk2')))	
				self.is_created = True
			except RawMaterialCheckRecord.DoesNotExist:
				pass
			return form_class(**self.get_form_kwargs())

	def form_valid(self, form):
		form.instance.batch = get_object_or_404(Batch, pk=self.kwargs.get('pk2'))

		try:
			form.save()
		except IntegrityError:
			pass
		return super(RawMaterialCheckView, self).form_valid(form)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['records'] = self.request.session['batch_records']
		context['batch'] = get_object_or_404(Batch, pk=self.kwargs.get('pk2'))
		context['product'] = get_object_or_404(Product, pk=self.kwargs.get('pk'))
		if self.is_created:
			context['raw_checks'] = RawMaterialCheckRecord.objects.filter(batch=get_object_or_404(Batch, pk=self.kwargs.get('pk2')))
		return context

	def get_success_url(self):
		product_id = self.kwargs.get('pk')
		batch_id = self.kwargs.get('pk2')
		return reverse_lazy('batches:raw-material-check', kwargs={'pk': product_id, 'pk2': batch_id})

@method_decorator(csrf_exempt, name="dispatch")
class RMCheckDelete(DeleteView):
	template_name = 'batch/rawmaterialcheckrecord_confirm_delete.html'
	model = RawMaterialCheckRecord
	context_object_name = 'raw_check'

	def get_object(self, *args, **kwargs):
		request = self.request
		pk = self.kwargs.get('pk3')
		instance = RawMaterialCheckRecord.objects.get(pk=pk)
		if instance is None:
			raise Http404('Batch Info could not be found')
		return instance

	def get_success_url(self):
		product_id = self.kwargs['pk']
		batch_id = self.kwargs.get('pk2')
		return reverse_lazy('batches:raw-material-check', kwargs={'pk': product_id, 'pk2': batch_id})

def process_control(request, pk, pk2, pk3=None):

	control_records = ControlRecords.objects.filter(batch=get_object_or_404(Batch, pk=pk2))
	cleaning_processes = CleaningProcess.objects.filter(batch=get_object_or_404(Batch, pk=pk2))

	try:
		individual_weight = IndividualWeight.objects.get(batch=get_object_or_404(Batch, pk=pk2))
		individual_weight_form = IndividualWeightForm(instance=individual_weight)
	except:
		individual_weight_form = IndividualWeightForm

	inprocess_control_form = InProcessControlForm
	cleaning_form = CleaningProcessForm

	context = {

		'batch': get_object_or_404(Batch, pk=pk2),
		'product': get_object_or_404(Product, pk=pk),
		'records': request.session['batch_records'],

		'control_records': control_records,
		'clean': cleaning_processes,

		'in_process_form': inprocess_control_form,
		'weight_form': individual_weight_form,
		'cleaning_form': cleaning_form,

	}

	if request.is_ajax() and request.method == "POST" and pk3:
		form = InProcessControlForm(request.POST)
		data = dict()
		control_record = ControlRecords.objects.get(pk=pk3)

		if form.is_valid():

			form = InProcessControlForm(request.POST, instance=control_record)
			form.save()
			data['form_is_valid'] = True
			data['messages'] = {'message': 'record updated successfully', 'type': 'success'}
			control_records = ControlRecords.objects.filter(batch=get_object_or_404(Batch, pk=pk2))

			context_dict = context.copy()
			context_dict['control_records'] = control_records

			data['html_control_list'] = render_to_string('batch/process_control.html', context_dict, request=request)
		else:
			data['form_is_valid'] = False

		return JsonResponse(data)

	if request.is_ajax() and request.method == 'POST':

		form = InProcessControlForm(request.POST)
		form.instance.batch = get_object_or_404(Batch, pk=pk2)
		try:
			saved_form = form.save()
		except IntegrityError:
			pass

		saved_instance = ControlRecords.objects.last()
		
		test = Specification.objects.get(pk=saved_instance.__dict__.get('test_id'))
		
		serialized_instance = serializers.serialize('json', [saved_instance,])

		data = {'messages':{'message': 'form saved successfully', 'type': 'success'}, 
				'test':{'test_name': test.test.name, 'specification': test.specification},
				'batch_data':{'batch_pk': pk2, 'product_pk': pk,
				'record_pk': saved_instance.pk}
				}

		return JsonResponse({'data': data, 'instance': serialized_instance})

	if request.is_ajax() and request.method == 'GET':

		control_record = get_object_or_404(ControlRecords, pk=pk3)
		form = InProcessControlForm(instance=control_record)
		context_dict = {
		'batch': get_object_or_404(Batch, pk=pk2),
		'product': get_object_or_404(Product, pk=pk),
		'record': control_record,
		'form': form
		}

		return JsonResponse({'form': render_to_string('helpers/control_update.html', context_dict, request=request)})
	
	return render(request, 'batch/process_control.html', context)

def control_delete(request, pk, pk2, pk3=None):

	data = dict()
	obj=None

	if pk3:
		obj = get_object_or_404(ControlRecords, pk=pk3)

	context = {
		'batch': get_object_or_404(Batch, pk=pk2),
		'product': get_object_or_404(Product, pk=pk),
		'record': obj,
	}

	if request.method == "POST":
		
		obj.delete()
		return HttpResponseRedirect(reverse_lazy('batches:process-control', kwargs={'pk': pk, 'pk2': pk2}))

	return render(request, 'batch/process_control_delete.html', context)

def individual_weight(request, pk, pk2):

	if request.is_ajax() and request.method == "POST":
		data = dict()
		form = IndividualWeightForm(request.POST)
		if form.is_valid():
			form.instance.batch = get_object_or_404(Batch, pk=pk2)
			try:
				form.save()
			except Exception as e:
				data['error']: str(e)
			data['success'] = "Weight saved!"

	return JsonResponse(data)

def cleaning(request, pk, pk2, pk3=None):

	try:
		individual_weight = IndividualWeight.objects.get(batch=get_object_or_404(Batch, pk=pk2))
		individual_weight_form = IndividualWeightForm(instance=individual_weight)
	except:
		individual_weight_form = IndividualWeightForm

	inprocess_control_form = InProcessControlForm
	cleaning_form = CleaningProcessForm

	context = {

		'batch': get_object_or_404(Batch, pk=pk2),
		'product': get_object_or_404(Product, pk=pk),
		'records': request.session['batch_records'],
		'control_records': ControlRecords.objects.filter(batch=get_object_or_404(Batch, pk=pk2)),

		'in_process_form': inprocess_control_form,
		'weight_form': individual_weight_form,
		'cleaning_form': cleaning_form,
	}

	if request.is_ajax() and request.method == "POST" and pk3:
		form = CleaningProcessForm(request.POST)
		data = dict()
		cleaning_process = CleaningProcess.objects.get(pk=pk3)

		if form.is_valid():

			form = CleaningProcessForm(request.POST, instance=cleaning_process)
			form.save()
			data['form_is_valid'] = True
			data['messages'] = {'message': 'process updated successfully', 'type': 'success'}
			processes = CleaningProcess.objects.filter(batch=get_object_or_404(Batch, pk=pk2))

			context_dict = context.copy()
			context_dict['clean'] = processes

			data['html_cleaning_list'] = render_to_string('batch/process_control.html', context_dict, request=request)
		else:
			data['form_is_valid'] = False

		return JsonResponse(data)

	if request.is_ajax() and request.method == "POST":

		data = dict()
		form = CleaningProcessForm(request.POST)

		if form.is_valid():
			form.instance.batch = get_object_or_404(Batch, pk=pk2)
			try:
				form.save()
			except Exception as e:
				data['error']: str(e)
			data['success'] = "Cleaning saved!"

			saved_instance = CleaningProcess.objects.last()

			serialized_instance = serializers.serialize('json', [saved_instance,])

			data['instance'] = serialized_instance

			data['batch_data'] = {'batch_pk': pk2, "product_pk": pk, "clean_pk": saved_instance.pk}

		return JsonResponse(data)

	if request.is_ajax() and request.method == "GET":

		cleaning_process = CleaningProcess.objects.get(pk=pk3)
		form = CleaningProcessForm(instance=cleaning_process)
		context['process'] = cleaning_process
		context['form'] = form

		return JsonResponse({'form': render_to_string('helpers/cleaning_update.html', context, request=request)})
	

def cleaning_delete(request, pk, pk2, pk3=None):

	data = dict()
	obj=None

	if pk3:
		obj = get_object_or_404(CleaningProcess, pk=pk3)

	context = {
		'batch': get_object_or_404(Batch, pk=pk2),
		'product': get_object_or_404(Product, pk=pk),
		'process': obj,
	}

	if request.method == "POST":
		
		obj.delete()
		return HttpResponseRedirect(reverse_lazy('batches:process-control', kwargs={'pk': pk, 'pk2': pk2}))

	return render(request, 'batch/cleaning_delete.html', context)

