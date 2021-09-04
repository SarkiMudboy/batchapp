from django.urls import path
from .views import ( product_list, 
                    ProductListView, 
                    ProductDetailView, 
                    ProductUpdateView, 
                    ProductDeleteView,
                    ProductCreateView )

app_name = 'products'

urlpatterns = [
    path('list/', ProductListView.as_view(), name='list'),
    path('list/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('list/<int:pk>/update', ProductUpdateView.as_view(), name='product-update'),
    path('list/<int:pk>/delete', ProductDeleteView.as_view(), name='product-delete'),
    path('list/create', ProductCreateView.as_view(), name='create-product')
]