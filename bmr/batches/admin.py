from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Batch)
admin.site.register(BatchInfoAuth)
admin.site.register(QualityControlAnalysis)
admin.site.register(ControlRecords)
admin.site.register(IndividualWeight)
admin.site.register(CleaningProcess)
admin.site.register(RawMaterialCheckRecord)
admin.site.register(RawMaterialPackagingBill)
admin.site.register(RawMaterialBillAuth)
admin.site.register(EquipmentCheck)
admin.site.register(EquipmentClearance)
admin.site.register(BatchManufacturingProcess)
admin.site.register(PackagingMaterial)
admin.site.register(BillOfPackaging)
admin.site.register(BatchPackagingProcess)
admin.site.register(BatchPackagingAuth)
admin.site.register(ProductYield)
admin.site.register(ProductSamples)
admin.site.register(ProductQuantitySale)
admin.site.register(ProductReconPackMaterials)
admin.site.register(ReleaseProfile)
admin.site.register(Guide)
