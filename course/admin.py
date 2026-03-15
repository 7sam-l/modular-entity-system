from django.contrib import admin
from core.admin import BaseModelAdmin
from .models import Course


@admin.register(Course)
class CourseAdmin(BaseModelAdmin):
    pass
