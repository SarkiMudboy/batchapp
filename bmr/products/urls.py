from django.urls import path
from .views import product_list, ProductListView, ProductDetailView

app_name = 'products'

urlpatterns = [
    path('list/', ProductListView.as_view(), name='list'),
    path('list/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
]