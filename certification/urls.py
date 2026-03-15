from django.urls import path
from .views import CertificationListView, CertificationDetailView

app_name = 'certification'

urlpatterns = [
    path('certifications/', CertificationListView.as_view(), name='certification-list'),
    path('certifications/<int:pk>/', CertificationDetailView.as_view(), name='certification-detail'),
]
