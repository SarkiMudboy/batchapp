from django.urls import path
from .views import ( product_list,
                    raw_materials,
                    equipment_list,
                    postEquipment,
                    create_raw_material,
                    ProductListView, 
                    ProductDetailView, 
                    ProductUpdateView, 
                    ProductDeleteView,
                    ProductCreateView,
                    EquipmentListView,
                    EquipmentCreateView,
                    EquipmentDetailView,
                    EquipmentDeleteView,
                    EquipmentUpdateView,
                    RawmaterialDetailView,
                    RawmaterialUpdateView,
                    RawmaterialDeleteView,
                     )

app_name = 'products'

urlpatterns = [
    # products
    path('list/', ProductListView.as_view(), name='list'),
    path('list/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('list/<int:pk>/update', ProductUpdateView.as_view(), name='product-update'),
    path('list/<int:pk>/delete', ProductDeleteView.as_view(), name='product-delete'),
    path('list/create', ProductCreateView.as_view(), name='create-product'),

    # equipments
    path('equipments/', equipment_list, name='equipments'),
    path('equipments/post/', postEquipment, name='post-equipment'),
    path('equipments/create', EquipmentCreateView.as_view(), name='create-equipment'),
    path('equipments/<int:pk>/', EquipmentDetailView.as_view(), name='equipment-detail'),
    path('equipments/<int:pk>/update', EquipmentUpdateView.as_view(), name='equipment-update'),
    path('equipments/<int:pk>/delete', EquipmentDeleteView.as_view(), name='equipment-delete'),

    # raw materials
    path('rawmaterials/', raw_materials, name='raw-materials'),
    path('rawmaterials/create', create_raw_material, name='create-rawmaterial'),
    path('rawmaterials/<int:pk>/', RawmaterialDetailView.as_view(), name='rawmaterial-detail'),
    path('rawmaterials/<int:pk>/update', RawmaterialUpdateView.as_view(), name='rawmaterial-update'),
    path('rawmaterials/<int:pk>/delete', RawmaterialDeleteView.as_view(), name='rawmaterial-delete')
]