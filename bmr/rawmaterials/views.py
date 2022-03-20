from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView, FormView
from .models import *

# Create your views here.

class RawmaterialView(ListView):
	template_name="templates/raw_material.html"
	model = Rawmaterial
	context_object_name = "raws"

class RawmaterialCreateView(CreateView):
	template_name="templates/raw_material_create.html"
	form_class = RawMaterialAppForm
	model = Rawmaterial

class RawmaterialUpdateView(UpdateView):
	template_name="templates/raw_material_update.html"
	form_class = RawMaterialAppForm
	model = Rawmaterial
	context_object_name = "raw"

class RawmaterialDeleteView(DeleteView):
	template_name="templates/raw_material_update.html"
	form_class = RawMaterialAppForm
	model = Rawmaterial
	context_object_name = "raw"


class RawMaterialBatchView(ListView):
	template_name="templates/raw_batch.html"
	model = Rawmaterial
	context_object_name = "raws"

class RawMaterialBatchCreate(CreateView):
	template_name="templates/raw_batch_create.html"
	form_class = RawMaterialAppForm
	model = Rawmaterial

class RawMaterialBatchUpdate(UpdateView):
	template_name="templates/raw_batch_update.html"
	form_class = RawMaterialAppForm
	model = Rawmaterial
	context_object_name = "raw"

class RawMaterialBatchDelete(DeleteView):
	template_name="templates/raw_batch_update.html"
	form_class = RawMaterialAppForm
	model = Rawmaterial
	context_object_name = "raw"