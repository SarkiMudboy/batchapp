from django.forms import ModelForm
from .models import Product, Equipment, RawMaterial


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