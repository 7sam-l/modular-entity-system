from django.contrib import admin
from core.admin import BaseModelAdmin
from .models import Certification


@admin.register(Certification)
class CertificationAdmin(BaseModelAdmin):
    pass
