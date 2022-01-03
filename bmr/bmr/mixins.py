from django.core import serializers
from django.http import JsonResponse, HttpResponse
from rawmaterials.models import RawMaterialBatch, Rawmaterial
from products.models import RawMaterial
import json

class AjaxFormMixin(object):
    def form_invalid(self, form):
        response = super(AjaxFormMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(AjaxFormMixin, self).form_valid(form)
        if self.request.is_ajax():
            print(form.cleaned_data)
            data = {
                'message': "Successfully submitted form data."
            }
            return JsonResponse(data)
        else:
            return response


def update_fields(instance, model, fields, includes_m2m=False):
	for field in fields:
		field_value = getattr(instance, field)

		if field_value:
			try:
				for obj in model.objects.filter(batch=instance.batch):
					setattr(obj, field, field_value)
					if includes_m2m:
						obj._callSignal = False
					obj.save()
			except:
				pass
		else:
			for obj in model.objects.filter(batch=instance.batch):
				if getattr(obj, field):
					setattr(instance, field, getattr(obj, field))
					if includes_m2m:
						instance._callSignal = False
						instance.save()
					break


def autocompleteModel(request):
	search_queryset = RawMaterialBatch.objects.filter(raw_material__name__startswith=request.GET.get('search'))
	results = []
	for result in search_queryset:
		query_result = RawMaterial.objects.get(name=result)
		results.append(query_result.name.raw_material.name + " " + str(query_result.standard_quantity)) 
	resp = request.GET['callback'] + '(' + json.dumps(results) + ');'
	return HttpResponse(resp, 'application/json')