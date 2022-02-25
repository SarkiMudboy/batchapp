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
from .models import (QualityControlAnalysis, Batch)
from .forms import (QCForm)


class QCView(FormView):
	template_name = 'extended_templates/quality_control.html'
	form_class = QCForm
	model = QualityControlAnalysis
	is_created = False

	def get_form(self, form_class=form_class):
		"""
		Check to see if the its an update request else return empty form
		"""
		if "pk3" in self.kwargs:
			qc_test = get_object_or_404(QualityControlAnalysis, pk=self.kwargs.get('pk3'))
			self.is_created = True
			return form_class(instance=qc_test, **self.get_form_kwargs())
		else:
			try:
				raw_materials = QualityControlAnalysis.objects.filter(batch=get_object_or_404(Batch, pk=self.kwargs.get('pk2')))	
				self.is_created = True
			except QualityControlAnalysis.DoesNotExist:
				pass
			return form_class(**self.get_form_kwargs())

	def form_valid(self, form):
		batch_obj = get_object_or_404(Batch, pk=self.kwargs.get('pk2'))
		form.instance.batch = batch_obj
		form.instance.product = batch_obj.product
		# add the orm for results_specification

		try:
			form.save()
		except IntegrityError:
			pass
		return super(QCView, self).form_valid(form)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['records'] = self.request.session['batch_records']
		context['batch'] = get_object_or_404(Batch, pk=self.kwargs.get('pk2'))
		context['product'] = get_object_or_404(Product, pk=self.kwargs.get('pk'))
		if self.is_created:
			context['results'] = QualityControlAnalysis.objects.filter(batch=get_object_or_404(Batch, pk=self.kwargs.get('pk2')))
		return context

	def get_success_url(self):
		product_id = self.kwargs.get('pk')
		batch_id = self.kwargs.get('pk2')
		return reverse_lazy('batches:qc-analysis-report', kwargs={'pk': product_id, 'pk2': batch_id})

@method_decorator(csrf_exempt, name="dispatch")
class QCDelete(DeleteView):
	template_name = 'extended_templates/qualitycontrolanalysis_confirm_delete.html'
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
