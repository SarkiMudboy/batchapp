from django.urls import path
from .views import (BatchProductListView, BatchListView, BatchCreateView, 
    BatchDeleteView, BatchUpdateView, BatchDetailView, BatchInfoView, BatchInfoDelete,
    ProductInitiationView, GuideView, GuideDelete, EquipmentCheckListView, EQCheckListDelete,
    )

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

]