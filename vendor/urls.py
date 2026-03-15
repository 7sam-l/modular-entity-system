from django.urls import path
from .views import VendorListView, VendorDetailView

app_name = 'vendor'

urlpatterns = [
    path('vendors/', VendorListView.as_view(), name='vendor-list'),
    path('vendors/<int:pk>/', VendorDetailView.as_view(), name='vendor-detail'),
]
