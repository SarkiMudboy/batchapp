from django.forms import ModelForm
from .models import Product


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