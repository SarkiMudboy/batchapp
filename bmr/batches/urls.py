from django.urls import path
from .views import BatchProductListView, BatchListView, BatchCreateView, BatchDeleteView, BatchUpdateView, BatchDetailView

app_name = 'batches'

urlpatterns = [
    path('batches/', BatchProductListView.as_view(), name='batch-products'),
    path('batches/<int:pk>/', BatchListView.as_view(), name='batches'),
    path('batches/<int:pk>/create', BatchCreateView.as_view(), name='batch-create'),
    path('batches/<int:pk>/<int:pk2>/update', BatchUpdateView.as_view(), name='batch-update'),
    path('batches/<int:pk>/<int:pk2>/delete', BatchDeleteView.as_view(), name='batch-delete'),
    path('batches/<int:pk>/<int:pk2>/', BatchDetailView.as_view(), name='batch-pages'),
]