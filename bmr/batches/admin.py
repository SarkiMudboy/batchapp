from django.contrib import admin
from .models import (
    Batch,
    Test,
    TestResult,
    QualityControlAnalysis,
    ControlRecords,
    IndividualWieght,
    CleaningProcess,
    InprocessAuth,
    RawMaterialBatch,
    RawMaterialCheckRecord,
    RawMaterialCheckRecordAuth,
    RawMaterialPackagingBill,
    RawMaterialBillAuth
)

# Register your models here.

admin.site.register(Batch)
admin.site.register(Test)
admin.site.register(TestResult)
admin.site.register(QualityControlAnalysis)
admin.site.register(ControlRecords)
admin.site.register(IndividualWieght)
admin.site.register(CleaningProcess)
admin.site.register(InprocessAuth)
admin.site.register(RawMaterialBatch)
admin.site.register(RawMaterialCheckRecord)
admin.site.register(RawMaterialCheckRecordAuth)
admin.site.register(RawMaterialPackagingBill)
admin.site.register(RawMaterialBillAuth)
