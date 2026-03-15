from django.urls import path
from .views import CourseCertificationMappingListView, CourseCertificationMappingDetailView

app_name = 'course_certification_mapping'

urlpatterns = [
    path('course-certification-mappings/', CourseCertificationMappingListView.as_view(), name='list'),
    path('course-certification-mappings/<int:pk>/', CourseCertificationMappingDetailView.as_view(), name='detail'),
]
