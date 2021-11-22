from django.forms import ModelForm
from django import forms
from .models import *


class BatchCreateForm(ModelForm):
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
        self.fields['production_commencement'].widget=forms.DateInput(format=('%Y-%m-%d'),
            attrs={'class': 'form-control', 
            'placeholder': 'Select a date',
            'type': 'date' })
        self.fields['production_completion'].widget=forms.DateInput(format=('%Y-%m-%d'),
            attrs={'class': 'form-control', 
            'placeholder': 'Select a date',
            'type': 'date' })
    
    class Meta:
        model = Batch
        exclude = ['product']


class BatchUpdateForm(ModelForm):
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
        self.fields['production_commencement'].widget=forms.DateInput(format=('%Y-%m-%d'),
            attrs={'class': 'form-control', 
            'placeholder': 'Select a date',
            'type': 'date' })
        self.fields['production_completion'].widget=forms.DateInput(format=('%Y-%m-%d'),
            attrs={'class': 'form-control', 
            'placeholder': 'Select a date',
            'type': 'date' })

    class Meta:
        model = Batch
        exclude = ['product']

class BatchRecordsCheckForm(forms.Form):
    # records
    pages = ['Batch Info', 'Production Initiation', 'Guide', 'Equipment Check List', 'Equipment Line Clearance', 
    'Master Formula Sheet', 'Bill of Raw Materials', 'Process', 'Raw Material Check', 'Process control', 'QC Analysis Report', 'Bill of packaging',
    'Product Reconiliation', 'Batch Release']

    BATCH_RECORDS = [(r , r) for r in pages]

    batch_records = forms.MultipleChoiceField(required=False, 
        widget=forms.CheckboxSelectMultiple, 
        choices=BATCH_RECORDS)

class BatchInfoForm(ModelForm):
    class Meta:
        model = BatchInfoAuth
        exclude = ['batch']

class GuideForm(ModelForm):
    class Meta:
        model = Guide
        exclude = ['batch']

class EquipmentCheckListForm(ModelForm):
    class Meta:
        model = EquipmentCheck
        exclude = ['batch']


