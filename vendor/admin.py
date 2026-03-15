from django.contrib import admin
from core.admin import BaseModelAdmin
from .models import Vendor


@admin.register(Vendor)
class VendorAdmin(BaseModelAdmin):
    pass
