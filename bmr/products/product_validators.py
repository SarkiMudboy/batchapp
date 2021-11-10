from django.core.exceptions import ValidationError
from .models import ManufacturingProcess, Product

def validate_step(step, product):
    products_process = ManufacturingProcess.objects.filter(products=product)
    for process in product_process:
        if process.step == step:
            raise ValidationError("A process with this step already exists!")

