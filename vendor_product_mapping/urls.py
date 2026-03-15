from django.urls import path
from .views import VendorProductMappingListView, VendorProductMappingDetailView

app_name = 'vendor_product_mapping'

urlpatterns = [
    path('vendor-product-mappings/', VendorProductMappingListView.as_view(), name='list'),
    path('vendor-product-mappings/<int:pk>/', VendorProductMappingDetailView.as_view(), name='detail'),
]
