from django.contrib import admin
from core.admin import BaseModelAdmin
from .models import Product


@admin.register(Product)
class ProductAdmin(BaseModelAdmin):
    pass
