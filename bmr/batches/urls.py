from django.urls import path
from .views import (BatchProductListView, BatchListView, BatchCreateView, 
    BatchDeleteView, BatchUpdateView, BatchDetailView, BatchInfoView, BatchInfoDelete,
    ProductInitiationView, GuideView, GuideDelete, EquipmentCheckListView, EQCheckListDelete,
    EquipmentClearanceView, EQClearanceDelete,
    )
from .extended_views import (MasterFormulaView, BillofRawMaterialView, RMBillDelete, BatchManufacturingView, 
    ProcessDelete, RawMaterialCheckView, RMCheckDelete, process_control, control_delete, individual_weight, 
    cleaning, cleaning_delete)

from .final_views import (
    QCView, QCDelete, QCCreateView, QCUpdate, PackagingBillCreateView, PackagingBillView, 
    PackagingProcessCreateView, PackagingBillUpdate, PackagingBillDelete, PackagingProcessUpdateView, 
    PackagingProcessDelete, PackagingMaterialView, PackagingMaterialUpdate, MaterialDelete, PackagingAuthView)

from .release_views import *
from .feature_views import *

app_name = 'batches'

urlpatterns = [
    path('batches/', BatchProductListView.as_view(), name='batch-products'),
    path('batches/<int:pk>/', BatchListView.as_view(), name='batches'),
    path('batches/<int:pk>/create', BatchCreateView.as_view(), name='batch-create'),
    path('batches/<int:pk>/<int:pk2>/update', BatchUpdateView.as_view(), name='batch-update'),
    path('batches/<int:pk>/<int:pk2>/delete', BatchDeleteView.as_view(), name='batch-delete'),
    path('batches/<int:pk>/<int:pk2>/', BatchDetailView.as_view(), name='batch-pages'),

    path('batches/<int:pk>/<int:pk2>/batch/', BatchInfoView.as_view(), name="batch-info"),
    path('batches/<int:pk>/<int:pk2>/batch/<int:pk3>/delete', BatchInfoDelete.as_view(), name="batch-info-delete"),
    
    path('batches/<int:pk>/<int:pk2>/product_init/', ProductInitiationView.as_view(), name="production-initiation"),
    
    path('batches/<int:pk>/<int:pk2>/guide/', GuideView.as_view(), name="guide"),
    path('batches/<int:pk>/<int:pk2>/guide/<int:pk3>/delete', GuideDelete.as_view(), name="guide-delete"),
    
    path('batches/<int:pk>/<int:pk2>/eq-check/', EquipmentCheckListView.as_view(), name="equipment-check-list"),
    path('batches/<int:pk>/<int:pk2>/eq-check/<int:pk3>/delete', EQCheckListDelete.as_view(), name="eq-check-delete"),
    path('batches/<int:pk>/<int:pk2>/eq-check/<int:pk3>/update', EquipmentCheckListView.as_view(), name="eq-check-update"),

    path('batches/<int:pk>/<int:pk2>/eq-clear/', EquipmentClearanceView.as_view(), name="equipment-line-clearance"),
    path('batches/<int:pk>/<int:pk2>/eq-clear/<int:pk3>/delete', EQClearanceDelete.as_view(), name="eq-clear-delete"),
    path('batches/<int:pk>/<int:pk2>/eq-clear/<int:pk3>/update', EquipmentClearanceView.as_view(), name="eq-clear-update"),

    path('batches/<int:pk>/<int:pk2>/formula/', MasterFormulaView.as_view(), name="master-formula-sheet"),

    path('batches/<int:pk>/<int:pk2>/raw-material-bill/', BillofRawMaterialView.as_view(), name="bill-of-raw-materials"),
    path('batches/<int:pk>/<int:pk2>/raw-material-bill/<int:pk3>/delete', RMBillDelete.as_view(), name="raw-bill-delete"),
    path('batches/<int:pk>/<int:pk2>/raw-material-bill/<int:pk3>/update', BillofRawMaterialView.as_view(), name="raw-bill-update"),

    path('batches/<int:pk>/<int:pk2>/process/', BatchManufacturingView.as_view(), name="process"),
    path('batches/<int:pk>/<int:pk2>/process/<int:pk3>/delete', ProcessDelete.as_view(), name="process-delete"),
    path('batches/<int:pk>/<int:pk2>/process/<int:pk3>/update', BatchManufacturingView.as_view(), name="process-update"),

    path('batches/<int:pk>/<int:pk2>/raw-material-check/', RawMaterialCheckView.as_view(), name="raw-material-check"),
    path('batches/<int:pk>/<int:pk2>/raw-material-check/<int:pk3>/delete', RMCheckDelete.as_view(), name="raw-check-delete"),
    path('batches/<int:pk>/<int:pk2>/raw-material-check/<int:pk3>/update', RawMaterialCheckView.as_view(), name="raw-check-update"),

    path('batches/<int:pk>/<int:pk2>/process-control/', process_control, name="process-control"),
    path('batches/<int:pk>/<int:pk2>/process-control/<int:pk3>/delete', control_delete, name="process-delete"),
    path('batches/<int:pk>/<int:pk2>/process-control/<int:pk3>/update', process_control, name="process-control-update"),

    path('batches/<int:pk>/<int:pk2>/individual-weight/', individual_weight, name="individual-weight"),

    path('batches/<int:pk>/<int:pk2>/cleaning-process/', cleaning, name="cleaning-process"),
    path('batches/<int:pk>/<int:pk2>/cleaning-process/<int:pk3>/update', cleaning, name="cleaning-update"),
    path('batches/<int:pk>/<int:pk2>/cleaning-process/<int:pk3>/delete', cleaning_delete, name="cleaning-delete"),

    path('batches/<int:pk>/<int:pk2>/qc-analysis-report/', QCView.as_view(), name="qc-analysis-report"),
    path('batches/<int:pk>/<int:pk2>/qc-analysis-report/<int:pk3>/update', QCUpdate.as_view(), name="qc-update"),
    path('batches/<int:pk>/<int:pk2>/qc-analysis-report/create', QCCreateView.as_view(), name="qc-create"),
    path('batches/<int:pk>/<int:pk2>/qc-analysis-report/<int:pk3>/delete', QCDelete.as_view(), name="qc-delete"),

    path('batches/<int:pk>/<int:pk2>/packaging-bill/', PackagingBillView.as_view(), name="bill-of-packaging"),
    path('batches/<int:pk>/<int:pk2>/packaging-bill/<int:pk3>/update', PackagingBillUpdate.as_view(), name="pack-bill-update"),
    path('batches/<int:pk>/<int:pk2>/packaging-bill/create', PackagingBillCreateView.as_view(), name="pack-bill-create"),
    path('batches/<int:pk>/<int:pk2>/packaging-bill/<int:pk3>/delete', PackagingBillDelete.as_view(), name="pack-bill-delete"),
    path('batches/<int:pk>/<int:pk2>/packaging-bill/process/create', PackagingProcessCreateView.as_view(), name="pack-process-create"),
    path('batches/<int:pk>/<int:pk2>/packaging-bill/process/<int:pk3>/update', PackagingProcessUpdateView.as_view(), name="pack-process-update"),
    path('batches/<int:pk>/<int:pk2>/packaging-bill/process/<int:pk3>/delete', PackagingProcessDelete.as_view(), name="pack-process-delete"),

    path('batches/<int:pk>/<int:pk2>/packaging-bill/material/create', PackagingMaterialView.as_view(), name="material-create"),
    path('batches/<int:pk>/<int:pk2>/packaging-bill/material/<int:pk3>/update', PackagingMaterialUpdate.as_view(), name="pack-material-update"),
    path('batches/<int:pk>/<int:pk2>/packaging-bill/material/<int:pk3>/delete', MaterialDelete.as_view(), name="material-delete"),

    path('batches/<int:pk>/<int:pk2>/packaging-bill/auth/', PackagingAuthView.as_view(), name="pack-auth"),

    # release urls
    path('batches/<int:pk>/<int:pk2>/product-recon/', ProductYieldView.as_view(), name='product-reconciliation'),
    path('batches/<int:pk>/<int:pk2>/product-recon/create', ProductYieldCreate.as_view(), name='product-recon-create'),
    path('batches/<int:pk>/<int:pk2>/product-recon/<int:pk3>/update', YieldUpdateView.as_view(), name='product-recon-update'),
    path('batches/<int:pk>/<int:pk2>/product-recon/<int:pk3>/delete', YieldDeleteView.as_view(), name='product-recon-delete'),

    path('batches/<int:pk>/<int:pk2>/product-recon/samples/create', ProductSampleCreate.as_view(), name='product-sample-create'),
    path('batches/<int:pk>/<int:pk2>/product-recon/samples/<int:pk3>/update', SampleUpdateView.as_view(), name='product-sample-update'),
    path('batches/<int:pk>/<int:pk2>/product-recon/samples/<int:pk3>/delete', SampleDeleteView.as_view(), name='product-sample-delete'),

    path('batches/<int:pk>/<int:pk2>/product-recon/sample-quantity/', QuantitySampleView.as_view(), name="quantity-sample"),

    path('batches/<int:pk>/<int:pk2>/product-recon/pack/create', ReconPackMaterialCreate.as_view(), name='recon-pack-create'),
    path('batches/<int:pk>/<int:pk2>/product-recon/pack/<int:pk3>/update', ReconPackMaterialUpdate.as_view(), name='recon-pack-update'),
    path('batches/<int:pk>/<int:pk2>/product-recon/pack/<int:pk3>/delete', ReconPackMaterialDelete.as_view(), name='recon-pack-delete'),

    path('batches/<int:pk>/<int:pk2>/batch-release/', BatchReleaseView.as_view(), name='batch-release'),
    path('batches/<int:pk>/<int:pk2>/batch-release/create', BatchReleaseCreate.as_view(), name='batch-release-create'),
    path('batches/<int:pk>/<int:pk2>/batch-release/<int:pk3>/update', BatchReleaseUpdate.as_view(), name='batch-release-update'),
    path('batches/<int:pk>/<int:pk2>/batch-release/<int:pk3>/delete', BatchReleaseDelete.as_view(), name='batch-release-delete'),

    # autofill 
    path('batches/<int:pk>/create/autofill', batch_autofill, name='batch-autofill'),
    path('batches/<int:pk>/<int:pk2>/batch/autofill', batch_info_autofill, name='batch-info-autofill'),
    path('batches/<int:pk>/<int:pk2>/guide/autofill', guide_autofill, name="guide-autofill"),
    path('batches/<int:pk>/<int:pk2>/eq-check/autofill', equipment_check_autofill, name='equipment-check-autofill'),
    path('batches/<int:pk>/<int:pk2>/eq-clear/autofill', equipment_clearance_autofill, name='equipment-clearance-autofill'),
    path('batches/<int:pk>/<int:pk2>/raw-material-bill/autofill', raw_bill_autofill, name='raw-bill-autofill'),

    path('batches/<int:pk>/<int:pk2>/process/autofill', batch_manufacturing_autofill, name='batch-process-autofill'),
    path('batches/<int:pk>/<int:pk2>/raw-material-check/autofill', raw_check_autofill, name='raw-check-autofill'),
    path('batches/<int:pk>/<int:pk2>/process-control/autofill', process_control_autofill, name='process-control-autofill'),
    path('batches/<int:pk>/<int:pk2>/cleaning-process/autofill', cleaning_process_autofill, name='clean-autofill'),
    path('batches/<int:pk>/<int:pk2>/qc-analysis-report/create/autofill', quality_control_autofill, name='qc-autofill'),
    path('batches/<int:pk>/<int:pk2>/packaging-bill/create/autofill', packaging_bill_autofill, name="pack-bill-autofill"),
    path('batches/<int:pk>/<int:pk2>/packaging-bill/process/create/autofill', packaging_process_autofill, name="pack-process-autofill"),
    path('batches/<int:pk>/<int:pk2>/packaging-bill/material/create/autofill', packaging_material_autofill, name="pack-material-autofill"),
    path('batches/<int:pk>/<int:pk2>/product-recon/create/autofill', product_yield_autofill, name="product-yield-autofill"),
    path('batches/<int:pk>/<int:pk2>/product-recon/samples/create/autofill', product_sample_autofill, name="product-sample-autofill"),
    path('batches/<int:pk>/<int:pk2>/product-recon/pack/create/autofill', recon_pack_autofill, name="recon-pack-autofill"),
    path('batches/<int:pk>/<int:pk2>/product-recon/sample-quantity/autofill', quantity_sale_autofill, name="qs-autofill"),
    path('batches/<int:pk>/<int:pk2>/batch-release/create/autofill', batch_release_autofill, name="batch-release-autofill"),
]