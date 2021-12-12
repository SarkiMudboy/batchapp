from django.forms import ModelForm
from django.core.exceptions import ValidationError
from .models import Product, Equipment, RawMaterial, Specification, Test, ManufacturingProcess

class ProductCreateForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class ProductUpdateForm(ModelForm):
    class Meta:
        model = Product
        fields = [
                    'product_name',
                    'generic_name',
                    'description', 
                    'unit_size',
                    'label_claim', 
                    'packaging', 
                    'product_type',
                    'product_for', 
                    'equipments',
                    'registration_number'
                ]

class EquipmentCreateForm(ModelForm):
    class Meta:
        model = Equipment
        fields = '__all__'


class EquipmentUpdateForm(ModelForm):
    class Meta:
        model = Equipment
        fields = ['name', 'id_num']

class RawmaterialCreateForm(ModelForm):
    class Meta:
        model = RawMaterial
        fields = '__all__'

class RawmaterialUpdateForm(ModelForm):
    class Meta:
        model = RawMaterial
        fields = '__all__'

class SpecificationCreateForm(ModelForm):
    class Meta:
        model = Specification
        exclude = ['product']

class SpecificationUpdateForm(ModelForm):
    class Meta:
        model = Specification
        exclude = ['product']

class TestCreateForm(ModelForm):
    class Meta:
        model = Test
        fields = '__all__'

class TestUpdateForm(ModelForm):
    class Meta:
        model = Test
        fields = ['name',]

class ProcessCreateForm(ModelForm):

    class Meta:
        model = ManufacturingProcess
        exclude = ['product', 'action_duration']

    def __init__(self, *args, **kwargs):
        self.request_kwargs = kwargs.pop('request_kwargs')
        super(ProcessCreateForm, self).__init__(*args, **kwargs)
        self.fields['action'].widget.attrs={
        'id': 'complete-id',
        'placeholder': 'Enter the step...'
        }

    def clean(self):
        cleaned_data = super(ProcessCreateForm, self).clean()
        product = Product.objects.get(pk=self.request_kwargs.get('pk'))
        print(product)
        processes = ManufacturingProcess.objects.filter(product=product)
        for process in processes:
            if process.step == cleaned_data.get('step'):
                raise ValidationError("A process with this step exists!")
        return cleaned_data


class ProcessUpdateForm(ModelForm):
    class Meta:
        model = ManufacturingProcess
        exclude = ['product', 'action_duration']

    def __init__(self, *args, **kwargs):
        self.request_kwargs = kwargs.pop('request_kwargs')
        super(ProcessUpdateForm, self).__init__(*args, **kwargs)
        self.fields['action'].widget.attrs={
        'id': 'complete-id',
        }

    def clean(self):
        cleaned_data = super(ProcessUpdateForm, self).clean()
        product = Product.objects.get(pk=self.request_kwargs.get('pk'))
        product_process = ManufacturingProcess.objects.get(pk=self.request_kwargs.get('pk2'))
        processes = ManufacturingProcess.objects.filter(product=product)
        for process in processes:
            if process.step == cleaned_data.get('step') and process.id != product_process.id:
                raise ValidationError("A process with this step exists!")
        return cleaned_data