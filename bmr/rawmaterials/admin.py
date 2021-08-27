from django.contrib import admin
from .models import RawMaterial, RawMaterialBatch

# Register your models here.

admin.site.register(RawMaterial)
admin.site.register(RawMaterialBatch)