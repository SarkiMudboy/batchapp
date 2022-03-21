from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView, FormView
from .models import *
from .forms import *

# Create your views here.

class RawmaterialView(ListView):
	template_name="rawmaterials/raw_material.html"
	model = Rawmaterial
	context_object_name = "raws"

class RawmaterialCreateView(CreateView):
	template_name="rawmaterials/raw_material_create.html"
	form_class = RawMaterialAppForm
	model = Rawmaterial
	success_url = reverse_lazy('raw_materials:raw-material-list')

class RawmaterialUpdateView(UpdateView):
	template_name="rawmaterials/raw_material_update.html"
	form_class = RawMaterialAppForm
	model = Rawmaterial
	context_object_name = "raw"
	success_url = reverse_lazy('raw_materials:raw-material-list')

class RawmaterialDeleteView(DeleteView):
	template_name="rawmaterials/raw_material_delete.html"
	model = Rawmaterial
	context_object_name = "raw"
	success_url = reverse_lazy('raw_materials:raw-material-list')


class RawMaterialBatchView(ListView):
	template_name="rawmaterials/raw_batch.html"
	model = RawMaterialBatch
	context_object_name = "batches"

class RawMaterialBatchCreate(CreateView):
	template_name="rawmaterials/raw_batch_create.html"
	form_class = RawMaterialBatchForm
	model = RawMaterialBatch
	success_url = reverse_lazy('raw_materials:raw-batch-list')

class RawMaterialBatchUpdate(UpdateView):
	template_name="rawmaterials/raw_batch_update.html"
	form_class = RawMaterialBatchForm
	model = RawMaterialBatch
	context_object_name = "batch"
	success_url = reverse_lazy('raw_materials:raw-batch-list')

class RawMaterialBatchDelete(DeleteView):
	template_name="rawmaterials/raw_batch_delete.html"
	model = RawMaterialBatch
	context_object_name = "batch"
	success_url = reverse_lazy('raw_materials:raw-batch-list')