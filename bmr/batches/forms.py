from django.forms import ModelForm
from django import forms
from bmr.mixins import update_fields
import datetime
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
    'Product Reconciliation', 'Batch Release']

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
        instance.save()

        # updates fields in other model instances from the db
        update_fields(instance, EquipmentClearance, ['last_product', 'next_product', 'quality_assurance_manager'])

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

        # updates fields in other model instances from the db
        update_fields(instance, RawMaterialBillAuth, ['approved_by'], includes_m2m=True)

        return instance

class ProcessForm(ModelForm):
    class Meta:
        model = BatchManufacturingProcess
        exclude = ['batch']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['action_from'].widget = forms.TimeInput(format='%H:%M',
            attrs={'class': 'form-control',
            'type': 'time', 
            'placeholder': 'Select time',})
        self.fields['action_to'].widget = forms.TimeInput(format='%H:%M',
            attrs={'class': 'form-control',
            'type': 'time', 
            'placeholder': 'Select time',})
        self.fields['manufacturing_commenced'].widget=forms.DateInput(format=('%Y-%m-%d'),
            attrs={'class': 'form-control', 
            'placeholder': 'Select a date',
            'type': 'date' })
        self.fields['manufacturing_completed'].widget=forms.DateInput(format=('%Y-%m-%d'),
            attrs={'class': 'form-control', 
            'placeholder': 'Select a date',
            'type': 'date' })


    def save(self, commit=True):

        instance = super(ProcessForm, self).save(commit=False)
        instance.save()

        # updates other fields in other model instances from the db
        update_fields(instance, BatchManufacturingProcess, ['manufacturing_commenced', 'manufacturing_completed', 'production_manager'])

        if commit:
            instance.save()

        return instance

class RawMaterialCheckForm(ModelForm):

    check_done_by = forms.ModelMultipleChoiceField(required=False, queryset=Staff.objects.all(), widget=forms.CheckboxSelectMultiple)
    
    class Meta:
        model = RawMaterialCheckRecord
        exclude = ['batch']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_tested'].widget=forms.DateInput(format=('%Y-%m-%d'),
            attrs={'class': 'form-control', 
            'placeholder': 'Select a date',
            'type': 'date' })

    def save(self, commit=True):
        instance = super(RawMaterialCheckForm, self).save(commit=False)

        instance._callSignal = True
        instance._form = self

        instance.save()

        # updates fields in other model instances from the db
        update_fields(instance, RawMaterialCheckRecord, ['assessment', 'total_assessment'], includes_m2m=True)

        return instance

class InProcessControlForm(ModelForm):
    class Meta:
        model = ControlRecords
        exclude = ['batch']

    def save(self, commit=True):
        instance = super(InProcessControlForm, self).save(commit=False)

        instance._callSignal = True
        instance._form = self

        instance.save()

        return instance

class IndividualWeightForm(ModelForm):
    class Meta:
        model = IndividualWeight
        exclude = ['batch', 'approved_by', 'checked_by']

    def save(self, commit=True):
        instance = super(IndividualWeightForm, self).save(commit=False)

        instance._callSignal = True
        instance._form = self

        instance.save()

        return instance

class CleaningProcessForm(ModelForm):
    class Meta:
        model = CleaningProcess
        exclude = ['batch', 'approved_by', 'checked_by']

    def save(self, commit=True):
        instance = super(CleaningProcessForm, self).save(commit=False)

        instance._callSignal = True
        instance._form = self

        instance.save()

        return instance

class QCForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.year = datetime.datetime.now().year
        self.CHOICES = ((1998+y, str(1998+y)) for y in range(self.year-1999))
        self.fields['pharmacopiea_specification_year']=forms.ChoiceField(choices=self.CHOICES, widget=forms.Select())

    class Meta:
        model = QualityControlAnalysis
        exclude = ['batch', 'product', 'result_specification']

    def save(self, commit=True):
        instance = super(QCForm, self).save(commit=False)

        instance._callSignal = False
        instance._form = self

        instance.save()

        update_fields(instance, QualityControlAnalysis, ['ar_number', 'result_pharmacopiea', 'pharmacopiea_specification_year', 'chemical_analyst',
            'microbiologist', 'quality_control_manager'])

        return instance


class PackagingCreateForm(ModelForm):
    
    class Meta:
        model = BillOfPackaging
        exclude = ['batch']

class PackagingProcessForm(ModelForm):
    class Meta:
        model = BatchPackagingProcess
        exclude = ['batch']

class PackagingMaterialForm(ModelForm):
    class Meta:
        model = PackagingMaterial
        exclude = ["batch"]

class PackagingAuthForm(ModelForm):
    class Meta:
        model = BatchPackagingAuth
        exclude = ["batch"]

class ProductYieldForm(ModelForm):
    class Meta:
        model = ProductYield
        exclude = ["batch"]

class ProductSampleForm(ModelForm):
    class Meta:
        model = ProductSamples
        exclude = ["batch"]

class PackagingAuthForm(ModelForm):
    class Meta:
        model = BatchPackagingAuth
        exclude = ["batch"]

class QuantitySaleForm(ModelForm):
    class Meta:
        model = ProductQuantitySale
        exclude = ["batch"]

class ReconPackMaterialForm(ModelForm):
    class Meta:
        model = ProductReconPackMaterials
        exclude = ["batch"]

    def save(self, commit=True):
        instance = super(ReconPackMaterialForm, self).save(commit=False)

        instance._callSignal = False
        instance._form = self

        instance.save()

        update_fields(instance, ProductReconPackMaterials, ['deviation', 'comments'])

        instance.save()

        return instance

class BatchReleaseForm(ModelForm):
    class Meta:
        model = ReleaseProfile
        exclude = ["batch"]

    def save(self, commit=True):
        instance = super(BatchReleaseForm, self).save(commit=False)

        instance._callSignal = False
        instance._form = self

        update_fields(instance, ReleaseProfile, ['quality_assurance_manager'])

        instance.save()

        return instance