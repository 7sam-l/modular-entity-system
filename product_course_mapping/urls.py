from django.urls import path
from .views import ProductCourseMappingListView, ProductCourseMappingDetailView

app_name = 'product_course_mapping'

urlpatterns = [
    path('product-course-mappings/', ProductCourseMappingListView.as_view(), name='list'),
    path('product-course-mappings/<int:pk>/', ProductCourseMappingDetailView.as_view(), name='detail'),
]
