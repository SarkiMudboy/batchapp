from django.forms import ModelForm
from .models import Product, Equipment, RawMaterial, Specification, Test
from bootstrap_modal_forms.forms import BSModalModelForm


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


class EquipmentUpdateForm(BSModalModelForm):
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
        fields = '__all__'

class SpecificationUpdateForm(ModelForm):
    class Meta:
        model = Specification
        fields = '__all__'

class TestCreateForm(ModelForm):
    class Meta:
        model = Test
        fields = '__all__'

class TestUpdateForm(ModelForm):
    class Meta:
        model = Test
        fields = '__all__'