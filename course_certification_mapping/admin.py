from django.contrib import admin
from core.admin import BaseMappingAdmin
from .models import CourseCertificationMapping


@admin.register(CourseCertificationMapping)
class CourseCertificationMappingAdmin(BaseMappingAdmin):
    list_display = ['id', 'course', 'certification', 'primary_mapping', 'is_active', 'created_at']
    search_fields = [
        'course__name', 'course__code',
        'certification__name', 'certification__code',
    ]
    raw_id_fields = ['course', 'certification']
