from django.contrib import admin
from .models import (
    Batch,
    BatchInfoAuth,
    TestResult,
    QualityControlAnalysis,
    ControlRecords,
    IndividualWieght,
    CleaningProcess,
    InprocessAuth,
    RawMaterialCheckRecord,
    RawMaterialCheckRecordAuth,
    RawMaterialPackagingBill,
    RawMaterialBillAuth,
    EquipmentCheck,
    EquipmentClearance,
    BatchManufacturingProcess,
    PackagingMaterial,
    BillOfPackaging,
    BatchPackagingProcess,
    BatchPackagingAuth,
    ProductReconciliation,
    ReleaseProfile,
    Guide
)

# Register your models here.

admin.site.register(Batch)
admin.site.register(BatchInfoAuth)
admin.site.register(TestResult)
admin.site.register(QualityControlAnalysis)
admin.site.register(ControlRecords)
admin.site.register(IndividualWieght)
admin.site.register(CleaningProcess)
admin.site.register(InprocessAuth)
admin.site.register(RawMaterialCheckRecord)
admin.site.register(RawMaterialCheckRecordAuth)
admin.site.register(RawMaterialPackagingBill)
admin.site.register(RawMaterialBillAuth)
admin.site.register(EquipmentCheck)
admin.site.register(EquipmentClearance)
admin.site.register(BatchManufacturingProcess)
admin.site.register(PackagingMaterial)
admin.site.register(BillOfPackaging)
admin.site.register(BatchPackagingProcess)
admin.site.register(BatchPackagingAuth)
admin.site.register(ProductReconciliation)
admin.site.register(ReleaseProfile)
admin.site.register(Guide)
