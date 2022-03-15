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
from .models import (QualityControlAnalysis, Batch, BillOfPackaging, BatchPackagingProcess)
from .forms import (QCForm, PackagingCreateForm, PackagingProcessForm)

import json


class QCCreateView(CreateView):
	template_name = "last_temp/quality_control_create.html"
	form_class = QCForm
	model = QualityControlAnalysis

	def get_success_url(self):
		product_id = self.kwargs.get('pk')
		batch_id = self.kwargs.get('pk2')
		return reverse_lazy('batches:qc-analysis-report', kwargs={'pk': product_id, 'pk2': batch_id})
	
	def form_valid(self, form):
		batch_obj = get_object_or_404(Batch, pk=self.kwargs.get('pk2'))
		form.instance.batch = batch_obj
		form.instance.product = batch_obj.product
		analysis_test = Specification.objects.filter(test__name=form.instance.test, product=batch_obj.product)
		test = list(analysis_test)[0]
		form.instance.result_specification = f"{test.specification}-{test.deviation} ({test.unit})"
		
		try:
			form.save()
		except IntegrityError:
			pass
		return super(QCCreateView, self).form_valid(form)


class QCView(ListView):
	template_name = 'last_temp/quality_control.html'
	form_class = QCForm
	model = QualityControlAnalysis

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['records'] = self.request.session['batch_records']
		context['batch'] = get_object_or_404(Batch, pk=self.kwargs.get('pk2'))
		context['product'] = get_object_or_404(Product, pk=self.kwargs.get('pk'))
		context['results'] = QualityControlAnalysis.objects.filter(batch=get_object_or_404(Batch, pk=self.kwargs.get('pk2')))
		return context


class QCUpdate(UpdateView):
	template_name = "last_temp/qc_update.html"
	form_class = QCForm
	model = QualityControlAnalysis

	def get_object(self, *args, **kwargs):
		request = self.request
		pk = self.kwargs.get('pk3')
		instance = QualityControlAnalysis.objects.get(pk=pk)
		if instance is None:
			raise Http404('Batch Info could not be found')
		return instance

	def get_success_url(self):
		product_id = self.kwargs.get('pk')
		batch_id = self.kwargs.get('pk2')
		return reverse_lazy('batches:qc-analysis-report', kwargs={'pk': product_id, 'pk2': batch_id})
	
	def form_valid(self, form):

		batch_obj = get_object_or_404(Batch, pk=self.kwargs.get('pk2'))
		form.instance.batch = batch_obj
		form.instance.product = batch_obj.product
		analysis_test = Specification.objects.filter(test__name=form.instance.test, product=batch_obj.product)
		test = list(analysis_test)[0]
		form.instance.result_specification = f"{test.specification}-{test.deviation} ({test.unit})"
		
		try:
			form.save()
		except IntegrityError:
			pass
		return super(QCUpdate, self).form_valid(form)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['batch'] = get_object_or_404(Batch, pk=self.kwargs.get('pk2'))
		context['product'] = get_object_or_404(Product, pk=self.kwargs.get('pk'))
		return context


@method_decorator(csrf_exempt, name="dispatch")
class QCDelete(DeleteView):
	template_name = 'last_temp/qualitycontrolanalysis_confirm_delete.html'
	model = QualityControlAnalysis
	context_object_name = 'result'

	def get_object(self, *args, **kwargs):
		request = self.request
		pk = self.kwargs.get('pk3')
		instance = QualityControlAnalysis.objects.get(pk=pk)
		if instance is None:
			raise Http404('Batch Info could not be found')
		return instance

	def get_success_url(self):
		product_id = self.kwargs['pk']
		batch_id = self.kwargs.get('pk2')
		return reverse_lazy('batches:qc-analysis-report', kwargs={'pk': product_id, 'pk2': batch_id})

class PackagingBillCreateView(CreateView, AjaxFormMixin):
	template_name = "last_temp/packaging_bill_create.html"
	model = BillOfPackaging
	form_class = PackagingCreateForm

	def form_valid(self, form):
		
		if self.request.is_ajax:
			
			batch_obj = get_object_or_404(Batch, pk=self.kwargs.get('pk2'))
			form.instance.batch = batch_obj

			try:
				form.save()
			except IntegrityError:
				pass
			
			obj = BillOfPackaging.objects.last()
			
			instance = {
				"material": obj.material.material,
				"quantity_required": obj.quantity_required,
				"actual_quantity": obj.actual_quantity,
				"action_by": obj.action_by.name,
				"checked_by": obj.checked_by.name
			}

			data = {
				"instance": json.dumps(instance),
				"object_data" : {"batch_pk": batch_obj.pk, "product_pk": self.kwargs.get('pk'), "bill_pk": obj.pk},
				'message': "Successfully submitted form data."
			}

			return JsonResponse(data)

		else:
			return super(AjaxFormMixin, self).form_valid(form)

	def get_success_url(self):
		product_id = self.kwargs['pk']
		batch_id = self.kwargs.get('pk2')
		return reverse_lazy('batches:bill-of-packaging', kwargs={'pk': product_id, 'pk2': batch_id})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['batch'] = get_object_or_404(Batch, pk=self.kwargs.get('pk2'))
		context['product'] = get_object_or_404(Product, pk=self.kwargs.get('pk'))
		return context

class PackagingBillView(ListView):
	template_name = "last_temp/packaging_bill.html"
	model = BillOfPackaging

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['batch'] = get_object_or_404(Batch, pk=self.kwargs.get('pk2'))
		context['product'] = get_object_or_404(Product, pk=self.kwargs.get('pk'))
		if BillOfPackaging.objects.all():
			context.update({"packaging_bills": BillOfPackaging.objects.all()})
		if BatchPackagingProcess.objects.all():
			context.update({"packaging_processes": BatchPackagingProcess.objects.all()})
		return context

class PackagingProcessCreateView(AjaxFormMixin, CreateView):
	
	template_name = "last_temp/packaging_process_form.html"
	model = BatchPackagingProcess
	form_class = PackagingProcessForm

	def form_valid(self, form):
		if self.request.is_ajax:
			
			batch_obj = get_object_or_404(Batch, pk=self.kwargs.get('pk2'))
			form.instance.batch = batch_obj

			try:
				form.save()
			except IntegrityError:
				pass
			
			obj = BatchPackagingProcess.objects.last()
			
			instance = {
				"process": obj.process,
				"action_by": obj.action_by.name,
				"checked_by": obj.checked_by.name
			}

			data = {
				"instance": json.dumps(instance),
				"object_data" : {"batch_pk": batch_obj.pk, "product_pk": self.kwargs.get('pk'), "process_pk": obj.pk},
				'message': "Successfully submitted form data."
			}

			return JsonResponse(data)

		else:
			return super(AjaxFormMixin, self).form_valid(form)

	def get_success_url(self):
		product_id = self.kwargs['pk']
		batch_id = self.kwargs.get('pk2')
		return reverse_lazy('batches:bill-of-packaging', kwargs={'pk': product_id, 'pk2': batch_id})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['batch'] = get_object_or_404(Batch, pk=self.kwargs.get('pk2'))
		context['product'] = get_object_or_404(Product, pk=self.kwargs.get('pk'))
		return context

class PackagingBillUpdate(AjaxFormMixin, UpdateView):
	template_name = "helpers/packaging_bill_update.html"
	model = BillOfPackaging
	form_class = PackagingCreateForm

	def get_object(self, *args, **kwargs):
		request = self.request
		pk = self.kwargs.get('pk3')
		instance = BillOfPackaging.objects.get(pk=pk)
		if instance is None:
			raise Http404('Batch Info could not be found')
		return instance

	def get(self, request, *args, **kwargs):

		instance = self.get_object()
		form = PackagingCreateForm(instance=instance)
		batch = get_object_or_404(Batch, pk=self.kwargs.get("pk2"))
		product = get_object_or_404(Product, pk=self.kwargs.get("pk"))

		context_dict = {
			'batch': batch,
			'product': product,
			'form': form,
			'bill': instance
		}

		return JsonResponse({'form': render_to_string('helpers/packaging_bill_update.html', context_dict, request=self.request)})

	def form_valid(self, form):

		response = super(AjaxFormMixin, self).form_valid(form)
		data = dict()

		if self.request.is_ajax():

			data["form_is_valid"] = True

			batch_obj = get_object_or_404(Batch, pk=self.kwargs.get('pk2'))
			form.instance.batch = batch_obj

			try:
				instance = form.save()
			except IntegrityError:
				pass
			
			bills = BillOfPackaging.objects.filter(batch=get_object_or_404(Batch, pk=self.kwargs.get("pk2")))
			
			try:
				process = BatchPackagingProcess.objects.filter(batch=get_object_or_404(Batch, pk=self.kwargs.get("pk2")))
			except:
				pass

			context_dict = self.get_context_data()
			context_dict['packaging_bills'] = bills
			context_dict['packaging_processes'] = process

			data['bill_template'] = render_to_string('last_temp/packaging_bill.html', context_dict, request=self.request)

		return JsonResponse(data)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["product"] = get_object_or_404(Product, pk=self.kwargs.get("pk"))
		context["batch"] = get_object_or_404(Batch, pk=self.kwargs.get("pk2"))
		return context

	def get_success_url(self):
		product_id = self.kwargs['pk']
		batch_id = self.kwargs.get('pk2')
		return reverse_lazy('batches:bill-of-packaging', kwargs={'pk': product_id, 'pk2': batch_id})

class PackagingBillDelete(DeleteView):
	template_name = 'last_temp/billofpackaging_confirm_delete.html'
	model = BillOfPackaging
	context_object_name = 'bill'

	def get_object(self, *args, **kwargs):
		request = self.request
		pk = self.kwargs.get('pk3')
		instance = BillOfPackaging.objects.get(pk=pk)
		if instance is None:
			raise Http404('Batch Info could not be found')
		return instance

	def get_success_url(self):
		product_id = self.kwargs['pk']
		batch_id = self.kwargs.get('pk2')
		return reverse_lazy('batches:bill-of-packaging', kwargs={'pk': product_id, 'pk2': batch_id})

class PackagingProcessUpdateView(AjaxFormMixin, UpdateView):
	template_name= "helpers/package_process_update.html"
	model = BatchPackagingProcess
	form_class = PackagingProcessForm
	
	def get_object(self, *args, **kwargs):
		request = self.request
		pk = self.kwargs.get('pk3')
		instance = BatchPackagingProcess.objects.get(pk=pk)
		if instance is None:
			raise Http404('Batch Info could not be found')
		return instance

	def get(self, request, *args, **kwargs):

		instance = self.get_object()
		form = PackagingProcessForm(instance=instance)
		batch = get_object_or_404(Batch, pk=self.kwargs.get("pk2"))
		product = get_object_or_404(Product, pk=self.kwargs.get("pk"))

		context_dict = {
			'batch': batch,
			'product': product,
			'form': form,
			'process': instance
		}

		return JsonResponse({'form': render_to_string('helpers/package_process_update.html', context_dict, request=self.request)})

	def form_valid(self, form):

		response = super(AjaxFormMixin, self).form_valid(form)
		data = dict()

		if self.request.is_ajax:

			data["form_is_valid"] = True

			batch_obj = get_object_or_404(Batch, pk=self.kwargs.get('pk2'))
			form.instance.batch = batch_obj

			try:
				instance = form.save()
			except IntegrityError:
				pass
			
			p = BatchPackagingProcess.objects.filter(batch=get_object_or_404(Batch, pk=self.kwargs.get("pk2")))
			bills = BillOfPackaging.objects.filter(batch=get_object_or_404(Batch, pk=self.kwargs.get("pk2")))

			context_dict = self.get_context_data()
			context_dict['packaging_processes'] = p
			context_dict['bills'] = bills

			data['process_template'] = render_to_string('last_temp/packaging_bill.html', context_dict, request=self.request)

		return JsonResponse(data)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["product"] = get_object_or_404(Product, pk=self.kwargs.get("pk"))
		context["batch"] = get_object_or_404(Batch, pk=self.kwargs.get("pk2"))
		return context

	def get_success_url(self):
		product_id = self.kwargs['pk']
		batch_id = self.kwargs.get('pk2')
		return reverse_lazy('batches:bill-of-packaging', kwargs={'pk': product_id, 'pk2': batch_id})