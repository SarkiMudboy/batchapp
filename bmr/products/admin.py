from django.contrib import admin
from .models import (
    Product,
    RawMaterial,
    Equipment,
    Specification,
    ManufacturingProcess
)

# Register your models here.

admin.site.register(Product)
admin.site.register(RawMaterial)
admin.site.register(Equipment)
admin.site.register(Specification)
admin.site.register(ManufacturingProcess)
