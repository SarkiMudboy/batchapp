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
    PackagingProcessView, PackagingBillUpdate, PackagingBillDelete)

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
    path('batches/<int:pk>/<int:pk2>/packaging-bill/process/create', PackagingProcessView.as_view(), name="pack-process-create"),
    path('batches/<int:pk>/<int:pk2>/packaging-bill/process/create', PackagingProcessView.as_view(), name="pack-process-update"),
]