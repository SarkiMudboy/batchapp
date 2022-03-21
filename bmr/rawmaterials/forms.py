from django.forms import ModelForm
from django import forms

from .models import *

class RawMaterialAppForm(ModelForm):
	class Meta:
		model = Rawmaterial
		fields = "__all__"

class RawMaterialBatchForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['manufacturing_date'].widget=forms.DateInput(format=('%Y-%m-%d'),
			attrs={'class': 'form-control', 
			'placeholder': 'Select a date',
			'type': 'date' })
		self.fields['expiry_date'].widget=forms.DateInput(format=('%Y-%m-%d'),
			attrs={'class': 'form-control', 
			'placeholder': 'Select a date',
			'type': 'date' })

	class Meta:
		model = RawMaterialBatch
		fields = "__all__"