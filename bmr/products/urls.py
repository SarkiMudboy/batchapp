from django.urls import path
from .views import ( product_list, raw_materials, equipment_list, postEquipment, create_raw_material, 
                    ProductListView, ProductDetailView, ProductUpdateView, 
                    ProductDeleteView, ProductCreateView, EquipmentListView, EquipmentCreateView, 
                    equipment_update, EquipmentDeleteView,EquipmentUpdateView,
                    RawmaterialDetailView, RawmaterialUpdateView,RawmaterialDeleteView,
                    ProductSpecificationDetailView, ProductSpecificationDeleteView,
                    ProductSpecificationListView,ProductSpecificationUpdateView,
                    ProductSpecificationCreateView,TestView, TestDetailView, 
                    TestCreateView, TestDeleteView, TestUpdateView
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
    path('equipments/<int:pk>/update', equipment_update, name='equipment-update'),
    path('equipments/<int:pk>/delete', EquipmentDeleteView.as_view(), name='equipment-delete'),

    # raw materials
    path('rawmaterials/', raw_materials, name='raw-materials'),
    path('rawmaterials/create', create_raw_material, name='create-rawmaterial'),
    path('rawmaterials/<int:pk>/', RawmaterialDetailView.as_view(), name='rawmaterial-detail'),
    path('rawmaterials/<int:pk>/update', RawmaterialUpdateView.as_view(), name='rawmaterial-update'),
    path('rawmaterials/<int:pk>/delete', RawmaterialDeleteView.as_view(), name='rawmaterial-delete'),

    # specifications
    path('list/<int:pk>/specs', ProductSpecificationListView.as_view(), name='specs'),
    path('list/<int:pk>/specs/create', ProductSpecificationCreateView.as_view(), name='create-spec'),
    path('list/<int:pk>/specs/<int:pk2>/', ProductSpecificationDetailView.as_view(), name='spec-detail'),
    path('list/<int:pk>/specs/<int:pk2>/update', ProductSpecificationUpdateView.as_view(), name='spec-update'),
    path('list/<int:pk>/specs/<int:pk2>/delete', ProductSpecificationDeleteView.as_view(), name='spec-delete'),

    # tests
    path('tests/', TestView, name='tests'),
    path('tests/create', TestCreateView, name='create-test'),
    path('tests/<int:pk>/', TestDetailView.as_view(), name='test-detail'),
    path('tests/<int:pk>/update', TestUpdateView.as_view(), name='test-update'),
    path('tests/<int:pk>/delete', TestDeleteView.as_view(), name='test-delete'),
]