from django.shortcuts import render, Http404
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponseRedirect
from django.forms.models import model_to_dict
from django.template.loader import render_to_string
from products.models import*
from .models import *
from .forms import *

def batch_autofill(request, pk):

	if request.is_ajax and request.method == "GET":
		try:
			query_set = Batch.objects.filter(product=get_object_or_404(Product, pk=pk))
			batch = list(query_set)[-1]
			form = BatchCreateForm(instance=batch)
			context_dict = {
				'product': get_object_or_404(Product, pk=pk),
				'form': form
			}

			return JsonResponse({'form': render_to_string('batches/batch_create.html', context_dict, request=request)})
		except Batch.DoesNotExist:
			return JsonResponse({"message": "No existing data!"})
		except IndexError:
			return JsonResponse({"message": "No existing data!"})


def batch_info_autofill(request, pk, pk2):

	if request.is_ajax and request.method == "GET":

		try:
			batches = Batch.objects.all()
			instance = BatchInfoAuth.objects.get(batch=list(batches)[-2])
			form = BatchInfoForm(instance=instance)

			context_dict = {
				'batch': get_object_or_404(Batch, pk=pk2),
				'product': get_object_or_404(Product, pk=pk),
				'form': form
			}
			
			return JsonResponse({'form': render_to_string('batch/batch_info.html', context_dict, request=request)})
		except BatchInfoAuth.DoesNotExist:
			return JsonResponse({"message": "No existing data!"})

def guide_autofill(request, pk, pk2):

	if request.is_ajax and request.method == "GET":

		try:
			batches = Batch.objects.all()
			instance = Guide.objects.get(batch=list(batches)[-2])
			form = GuideForm(instance=instance)

			context_dict = {
				'batch': get_object_or_404(Batch, pk=pk2),
				'product': get_object_or_404(Product, pk=pk),
				'form': form
			}
			
			return JsonResponse({'form': render_to_string('batch/guide.html', context_dict, request=request)})
		except Guide.DoesNotExist:
			return JsonResponse({"message": "No existing data!"})


def equipment_check_autofill(request, pk, pk2):

	if request.is_ajax and request.method == "GET":

		try:
			batches = Batch.objects.all()
			query_set = EquipmentCheck.objects.filter(batch=list(batches)[-2])
			instance = list(query_set)[-1]
			form = EquipmentCheckListForm(instance=instance)

			context_dict = {
				'batch': get_object_or_404(Batch, pk=pk2),
				'product': get_object_or_404(Product, pk=pk),
				'form': form
			}
			
			return JsonResponse({'form': render_to_string('batch/equipment_check_list.html', context_dict, request=request)})
		except EquipmentCheck.DoesNotExist:
			return JsonResponse({"message": "No existing data!"})
		except IndexError:
			return JsonResponse({"message": "No existing data!"})


def equipment_clearance_autofill(request, pk, pk2):

	if request.is_ajax and request.method == "GET":

		try:
			batches = Batch.objects.all()
			query_set = EquipmentClearance.objects.filter(batch=list(batches)[-2])
			instance = list(query_set)[-1]
			form = EquipmentClearanceForm(instance=instance)

			context_dict = {
				'batch': get_object_or_404(Batch, pk=pk2),
				'product': get_object_or_404(Product, pk=pk),
				'form': form
			}
			
			return JsonResponse({'form': render_to_string('batch/equipment_clearance.html', context_dict, request=request)})
		except EquipmentClearance.DoesNotExist:
			return JsonResponse({"message": "No existing data!"})
		except IndexError:
			return JsonResponse({"message": "No existing data!"})


def raw_bill_autofill(request, pk, pk2):

	if request.is_ajax and request.method == "GET":

		try:
			batches = Batch.objects.all()
			query_set = RawMaterialBillAuth.objects.filter(batch=list(batches)[-2])
			instance = list(query_set)[-1]
			form = RawMaterialBillForm(instance=instance)

			context_dict = {
				'batch': get_object_or_404(Batch, pk=pk2),
				'product': get_object_or_404(Product, pk=pk),
				'form': form
			}
			
			return JsonResponse({'form': render_to_string('batch/equipment_clearance.html', context_dict, request=request)})
		except RawMaterialBillAuth.DoesNotExist:
			return JsonResponse({"message": "No existing data!"})
		except IndexError:
			return JsonResponse({"message": "No existing data!"})

def batch_manufacturing_autofill(request, pk, pk2):

	if request.is_ajax and request.method == "GET":

		try:
			batches = Batch.objects.all()
			query_set = BatchManufacturingProcess.objects.filter(batch=list(batches)[-2])
			instance = list(query_set)[-1]
			form = ProcessForm(instance=instance)

			context_dict = {
				'batch': get_object_or_404(Batch, pk=pk2),
				'product': get_object_or_404(Product, pk=pk),
				'form': form
			}
			
			return JsonResponse({'form': render_to_string('batch/batch_process.html', context_dict, request=request)})
		except BatchManufacturingProcess.DoesNotExist:
			return JsonResponse({"message": "No existing data!"})
		except IndexError:
			return JsonResponse({"message": "No existing data!"})


def raw_check_autofill(request, pk, pk2):

	if request.is_ajax and request.method == "GET":

		try:
			batches = Batch.objects.all()
			query_set = RawMaterialCheckRecord.objects.filter(batch=list(batches)[-2])
			instance = list(query_set)[-1]
			form = RawMaterialCheckForm(instance=instance)

			context_dict = {
				'batch': get_object_or_404(Batch, pk=pk2),
				'product': get_object_or_404(Product, pk=pk),
				'form': form
			}
			
			return JsonResponse({'form': render_to_string('batch/raw_material_check.html', context_dict, request=request)})
		except RawMaterialCheckRecord.DoesNotExist:
			return JsonResponse({"message": "No existing data!"})
		except IndexError:
			return JsonResponse({"message": "No existing data!"})

def raw_check_autofill(request, pk, pk2):

	if request.is_ajax and request.method == "GET":

		try:
			batches = Batch.objects.all()
			query_set = ControlRecords.objects.filter(batch=list(batches)[-2])
			instance = list(query_set)[-1]
			form = InProcessControlForm(instance=instance)

			context_dict = {
				'batch': get_object_or_404(Batch, pk=pk2),
				'product': get_object_or_404(Product, pk=pk),
				'form': form
			}
			
			return JsonResponse({'form': render_to_string('batch/raw_material_check.html', context_dict, request=request)})
		except RawMaterialCheckRecord.DoesNotExist:
			return JsonResponse({"message": "No existing data!"})
		except IndexError:
			return JsonResponse({"message": "No existing data!"})

def process_control_autofill(request, pk, pk2):

	if request.is_ajax and request.method == "GET":

		try:
			batches = Batch.objects.all()
			query_set = ControlRecords.objects.filter(batch=list(batches)[-2])
			instance = list(query_set)[-1]
			form = InProcessControlForm(instance=instance)

			context_dict = {
				'batch': get_object_or_404(Batch, pk=pk2),
				'product': get_object_or_404(Product, pk=pk),
				'form': form
			}
			
			return JsonResponse({'form': render_to_string('auto_fill/process-control-partial.html', context_dict, request=request)})
		except ControlRecords.DoesNotExist:
			return JsonResponse({"message": "No existing data!"})
		except IndexError:
			return JsonResponse({"message": "No existing data!"})

def cleaning_process_autofill(request, pk, pk2):

	if request.is_ajax and request.method == "GET":

		try:
			batches = Batch.objects.all()
			query_set = CleaningProcess.objects.filter(batch=list(batches)[-2])
			instance = list(query_set)[-1]
			form = CleaningProcessForm(instance=instance)

			context_dict = {
				'batch': get_object_or_404(Batch, pk=pk2),
				'product': get_object_or_404(Product, pk=pk),
				'cleaning_form': form
			}
			
			return JsonResponse({'form': render_to_string('auto_fill/clean_autofill.html', context_dict, request=request)})
		except CleaningProcess.DoesNotExist:
			return JsonResponse({"message": "No existing data!"})
		except IndexError:
			return JsonResponse({"message": "No existing data!"})

def quality_control_autofill(request, pk, pk2):

	if request.is_ajax and request.method == "GET":

		try:
			batches = Batch.objects.all()
			query_set = QualityControlAnalysis.objects.filter(batch=list(batches)[-2])
			instance = list(query_set)[-1]
			form = QCForm(instance=instance)

			context_dict = {
				'batch': get_object_or_404(Batch, pk=pk2),
				'product': get_object_or_404(Product, pk=pk),
				'form': form
			}
			
			return JsonResponse({'form': render_to_string('last_temp/quality_control_create.html', context_dict, request=request)})
		except QualityControlAnalysis.DoesNotExist:
			return JsonResponse({"message": "No existing data!"})
		except IndexError:
			return JsonResponse({"message": "No existing data!"})

def packaging_bill_autofill(request, pk, pk2):

	if request.is_ajax and request.method == "GET":

		try:
			batches = Batch.objects.all()
			query_set = BillOfPackaging.objects.filter(batch=list(batches)[-2])
			instance = list(query_set)[-1]
			form = PackagingCreateForm(instance=instance)

			context_dict = {
				'batch': get_object_or_404(Batch, pk=pk2),
				'product': get_object_or_404(Product, pk=pk),
				'form': form
			}
			
			return JsonResponse({'form': render_to_string('last_temp/packaging_bill_create.html', context_dict, request=request)})
		except BillOfPackaging.DoesNotExist:
			return JsonResponse({"message": "No existing data!"})
		except IndexError:
			return JsonResponse({"message": "No existing data!"})

def packaging_process_autofill(request, pk, pk2):

	if request.is_ajax and request.method == "GET":

		try:
			batches = Batch.objects.all()
			query_set = BatchPackagingProcess.objects.filter(batch=list(batches)[-2])
			instance = list(query_set)[-1]
			form = PackagingProcessForm(instance=instance)

			context_dict = {
				'batch': get_object_or_404(Batch, pk=pk2),
				'product': get_object_or_404(Product, pk=pk),
				'form': form
			}
			
			return JsonResponse({'form': render_to_string('last_temp/packaging_process_form.html', context_dict, request=request)})
		except BatchPackagingProcess.DoesNotExist:
			return JsonResponse({"message": "No existing data!"})
		except IndexError:
			return JsonResponse({"message": "No existing data!"})


def packaging_material_autofill(request, pk, pk2):

	if request.is_ajax and request.method == "GET":

		try:
			batches = Batch.objects.all()
			query_set = PackagingMaterial.objects.filter(batch=list(batches)[-2])
			instance = list(query_set)[-1]
			form = PackagingMaterialForm(instance=instance)

			context_dict = {
				'batch': get_object_or_404(Batch, pk=pk2),
				'product': get_object_or_404(Product, pk=pk),
				'form': form
			}
			
			return JsonResponse({'form': render_to_string('last_temp/material_create.html', context_dict, request=request)})
		except PackagingMaterial.DoesNotExist:
			return JsonResponse({"message": "No existing data!"})
		except IndexError:
			return JsonResponse({"message": "No existing data!"})

def product_yield_autofill(request, pk, pk2):

	if request.is_ajax and request.method == "GET":

		try:
			batches = Batch.objects.all()
			query_set = ProductYield.objects.filter(batch=list(batches)[-2])
			instance = list(query_set)[-1]
			form = ProductYieldForm(instance=instance)

			context_dict = {
				'batch': get_object_or_404(Batch, pk=pk2),
				'product': get_object_or_404(Product, pk=pk),
				'form': form
			}
			
			return JsonResponse({'form': render_to_string('last_temp/product_yield_create.html', context_dict, request=request)})
		except ProductYield.DoesNotExist:
			return JsonResponse({"message": "No existing data!"})
		except IndexError:
			return JsonResponse({"message": "No existing data!"})

def product_sample_autofill(request, pk, pk2):

	if request.is_ajax and request.method == "GET":

		try:
			batches = Batch.objects.all()
			query_set = ProductSamples.objects.filter(batch=list(batches)[-2])
			instance = list(query_set)[-1]
			form = ProductSampleForm(instance=instance)

			context_dict = {
				'batch': get_object_or_404(Batch, pk=pk2),
				'product': get_object_or_404(Product, pk=pk),
				'form': form
			}
			
			return JsonResponse({'form': render_to_string('last_temp/product_sample_create.html', context_dict, request=request)})
		except ProductSamples.DoesNotExist:
			return JsonResponse({"message": "No existing data!"})
		except IndexError:
			return JsonResponse({"message": "No existing data!"})


def recon_pack_autofill(request, pk, pk2):

	if request.is_ajax and request.method == "GET":

		try:
			batches = Batch.objects.all()
			query_set = ProductReconPackMaterials.objects.filter(batch=list(batches)[-2])
			instance = list(query_set)[-1]
			form = ReconPackMaterialForm(instance=instance)

			context_dict = {
				'batch': get_object_or_404(Batch, pk=pk2),
				'product': get_object_or_404(Product, pk=pk),
				'form': form
			}
			
			return JsonResponse({'form': render_to_string('last_temp/recon_pack_create.html', context_dict, request=request)})
		except ProductReconPackMaterials.DoesNotExist:
			return JsonResponse({"message": "No existing data!"})
		except IndexError:
			return JsonResponse({"message": "No existing data!"})

def quantity_sale_autofill(request, pk, pk2):

	if request.is_ajax and request.method == "GET":

		try:
			batches = Batch.objects.all()
			query_set = ProductQuantitySale.objects.filter(batch=list(batches)[-2])
			instance = list(query_set)[-1]
			form = QuantitySaleForm(instance=instance)

			context_dict = {
				'batch': get_object_or_404(Batch, pk=pk2),
				'product': get_object_or_404(Product, pk=pk),
				'quantity_sale_form': form
			}
			
			return JsonResponse({'form': render_to_string('auto_fill/qs_autofill.html', context_dict, request=request)})
		except ProductQuantitySale.DoesNotExist:
			return JsonResponse({"message": "No existing data!"})
		except IndexError:
			return JsonResponse({"message": "No existing data!"})

def batch_release_autofill(request, pk, pk2):

	if request.is_ajax and request.method == "GET":

		try:
			batches = Batch.objects.all()
			query_set = ReleaseProfile.objects.filter(batch=list(batches)[-2])
			instance = list(query_set)[-1]
			form = BatchReleaseForm(instance=instance)

			context_dict = {
				'batch': get_object_or_404(Batch, pk=pk2),
				'product': get_object_or_404(Product, pk=pk),
				'form': form
			}
			
			return JsonResponse({'form': render_to_string('last_temp/release_profile_create.html', context_dict, request=request)})
		except ReleaseProfile.DoesNotExist:
			return JsonResponse({"message": "No existing data!"})
		except IndexError:
			return JsonResponse({"message": "No existing data!"})