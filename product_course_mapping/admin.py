from django.contrib import admin
from core.admin import BaseMappingAdmin
from .models import ProductCourseMapping


@admin.register(ProductCourseMapping)
class ProductCourseMappingAdmin(BaseMappingAdmin):
    list_display = ['id', 'product', 'course', 'primary_mapping', 'is_active', 'created_at']
    search_fields = [
        'product__name', 'product__code',
        'course__name', 'course__code',
    ]
    raw_id_fields = ['product', 'course']
