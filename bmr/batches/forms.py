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

class EquipmentClearanceForm(ModelForm):
    class Meta:
        model = EquipmentClearance
        exclude = ['batch']

    def save(self, commit=True):
        instance = super(EquipmentClearanceForm, self).save(commit=False)

        last_product = instance.last_product
        next_product = instance.next_product
        qa_manager = instance.quality_assurance_manager

        if last_product:
            try:
                for clearance in EquipmentClearance.objects.filter(batch=instance.batch):
                    clearance.last_product = last_product
                    clearance.save()
            except:
                pass
        else:
            for clearance in EquipmentClearance.objects.filter(batch=instance.batch):
                if clearance.last_product:
                    instance.last_product = clearance.last_product
                    break

        if next_product:
            try:
                for clearance in EquipmentClearance.objects.filter(batch=instance.batch):
                    clearance.next_product = next_product
                    clearance.save()
            except:
                pass
        else:
            for clearance in EquipmentClearance.objects.filter(batch=instance.batch):
                if clearance.next_product:
                    instance.next_product = clearance.next_product
                    break

        if qa_manager:
            try:
                for clearance in EquipmentClearance.objects.filter(batch=instance.batch):
                    clearance.quality_assurance_manager = qa_manager
                    clearance.save()
            except:
                pass
        else:
            for clearance in EquipmentClearance.objects.filter(batch=instance.batch):
                if clearance.quality_assurance_manager:
                    instance.quality_assurance_manager = clearance.quality_assurance_manager
                    break

        if commit:
            instance.save()

        return instance

class RawMaterialBillForm(ModelForm):

    confirmed_by = forms.ModelMultipleChoiceField(required=False, queryset=Staff.objects.all(), widget=forms.CheckboxSelectMultiple)
    
    class Meta:
        model = RawMaterialBillAuth
        exclude = ['batch']

    def save(self, commit=True):
        instance = super(RawMaterialBillForm, self).save(commit=False)

        instance._callSignal = True
        instance._form = self

        instance.save()

        approved_by = instance.approved_by

        if approved_by:
            try:
                for bill in RawMaterialBillAuth.objects.filter(batch=instance.batch):
                    bill.approved_by = approved_by
                    bill._callSignal = False
                    bill.save()
            except:
                pass
        else:
            for bill in RawMaterialBillAuth.objects.filter(batch=instance.batch):
                if bill.approved_by:
                    instance.approved_by = bill.approved_by
                    instance._callSignal = False
                    instance.save()
                    break

        return instance