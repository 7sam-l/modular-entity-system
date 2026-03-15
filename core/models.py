"""
Abstract base models shared by every app in the project.
"""

from django.db import models
from .constants import CODE_MAX_LENGTH, NAME_MAX_LENGTH


class TimestampedModel(models.Model):
    """Adds auto-managed created_at / updated_at to any model."""

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class MasterModel(TimestampedModel):
    """
    Common fields for all master entities.
    (Vendor, Product, Course, Certification)
    """

    name = models.CharField(max_length=NAME_MAX_LENGTH)
    code = models.CharField(max_length=CODE_MAX_LENGTH, unique=True, db_index=True)
    description = models.TextField(blank=True, default='')
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'{self.name} ({self.code})'

    def soft_delete(self) -> None:
        """Deactivate without removing the database row."""
        self.is_active = False
        self.save(update_fields=['is_active', 'updated_at'])


class MappingModel(TimestampedModel):
    """
    Common fields for all mapping entities.
    (VendorProductMapping, ProductCourseMapping, CourseCertificationMapping)
    """

    primary_mapping = models.BooleanField(default=False, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def soft_delete(self) -> None:
        """Deactivate without removing the database row."""
        self.is_active = False
        self.save(update_fields=['is_active', 'updated_at'])
