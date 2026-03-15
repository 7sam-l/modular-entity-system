from django.contrib import admin
from core.admin import BaseMappingAdmin
from .models import VendorProductMapping


@admin.register(VendorProductMapping)
class VendorProductMappingAdmin(BaseMappingAdmin):
    list_display = ['id', 'vendor', 'product', 'primary_mapping', 'is_active', 'created_at']
    search_fields = [
        'vendor__name', 'vendor__code',
        'product__name', 'product__code',
    ]
    raw_id_fields = ['vendor', 'product']
