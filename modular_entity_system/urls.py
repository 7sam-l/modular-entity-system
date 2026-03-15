"""
Root URL configuration for modular_entity_system.
"""
from django.http import JsonResponse
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

def home(request):
    return JsonResponse({
        "message": "Modular Entity System API",
        "swagger": "/swagger/",
        "redoc": "/redoc/"
    })

# ─── Admin site branding ───────────────────────────────────────────────────────

admin.site.site_header = getattr(settings, 'ADMIN_SITE_HEADER', 'Administration')
admin.site.site_title = getattr(settings, 'ADMIN_SITE_TITLE', 'Admin')
admin.site.index_title = getattr(settings, 'ADMIN_INDEX_TITLE', 'Dashboard')

# ─── OpenAPI / Swagger ─────────────────────────────────────────────────────────

api_info = openapi.Info(
    title='Modular Entity System API',
    default_version='v1',
    description=(
        'A modular Django REST Framework backend managing **Vendors, Products, '
        'Courses, and Certifications** and their relationships.\n\n'
        '**Hierarchy:** `Vendor → Product → Course → Certification`\n\n'
        'All list endpoints support **pagination** (`?page=1&page_size=20`) '
        'and **soft-delete** via `is_active`.'
    ),
    terms_of_service='https://www.example.com/terms/',
    contact=openapi.Contact(email='admin@example.com'),
    license=openapi.License(name='MIT License'),
)

schema_view = get_schema_view(
    api_info,
    public=True,
    permission_classes=[permissions.AllowAny],
)

# ─── URL patterns ──────────────────────────────────────────────────────────────

urlpatterns = [
    path('', home),

    # Django admin
    path('admin/', admin.site.urls),

    # Swagger / ReDoc
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),

    # System
    path('api/', include('core.urls')),

    # Master entities
    path('api/', include('vendor.urls')),
    path('api/', include('product.urls')),
    path('api/', include('course.urls')),
    path('api/', include('certification.urls')),

    # Mapping entities
    path('api/', include('vendor_product_mapping.urls')),
    path('api/', include('product_course_mapping.urls')),
    path('api/', include('course_certification_mapping.urls')),
]
