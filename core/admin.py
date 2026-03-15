"""
Base ModelAdmin classes registered for core and inherited by every app.
"""

from django.contrib import admin


class BaseModelAdmin(admin.ModelAdmin):
    """
    Shared admin config for master entities.
    Each app's admin only needs to extend this and set model-specific fields.
    """

    list_display = ['id', 'name', 'code', 'is_active', 'created_at', 'updated_at']
    list_display_links = ['id', 'name']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'code']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    list_per_page = 25

    # Allow toggling is_active directly from the list view
    actions = ['mark_active', 'mark_inactive']

    @admin.action(description='Mark selected as active')
    def mark_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} record(s) marked as active.')

    @admin.action(description='Mark selected as inactive (soft delete)')
    def mark_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} record(s) marked as inactive.')


class BaseMappingAdmin(admin.ModelAdmin):
    """
    Shared admin config for mapping entities.
    """

    list_filter = ['primary_mapping', 'is_active', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    list_per_page = 25

    actions = ['mark_active', 'mark_inactive', 'set_primary', 'unset_primary']

    @admin.action(description='Mark selected as active')
    def mark_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description='Mark selected as inactive')
    def mark_inactive(self, request, queryset):
        queryset.update(is_active=False)

    @admin.action(description='Set primary_mapping = True')
    def set_primary(self, request, queryset):
        queryset.update(primary_mapping=True)

    @admin.action(description='Set primary_mapping = False')
    def unset_primary(self, request, queryset):
        queryset.update(primary_mapping=False)
