"""
Reusable drf-yasg openapi schema builders.

Instead of copy-pasting openapi.Schema blocks in every views.py, import
these factory functions. Each function returns an openapi.Response or
openapi.Schema object ready for use in @swagger_auto_schema decorators.
"""

from drf_yasg import openapi

# ─── Shared field schemas ──────────────────────────────────────────────────────

_MASTER_PROPERTIES = {
    'id': openapi.Schema(type=openapi.TYPE_INTEGER, read_only=True),
    'name': openapi.Schema(type=openapi.TYPE_STRING),
    'code': openapi.Schema(type=openapi.TYPE_STRING),
    'description': openapi.Schema(type=openapi.TYPE_STRING),
    'is_active': openapi.Schema(type=openapi.TYPE_BOOLEAN),
    'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', read_only=True),
    'updated_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', read_only=True),
}

_MAPPING_BASE_PROPERTIES = {
    'id': openapi.Schema(type=openapi.TYPE_INTEGER, read_only=True),
    'primary_mapping': openapi.Schema(type=openapi.TYPE_BOOLEAN, default=False),
    'is_active': openapi.Schema(type=openapi.TYPE_BOOLEAN, default=True),
    'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', read_only=True),
    'updated_at': openapi.Schema(type=openapi.TYPE_STRING, format='date-time', read_only=True),
}

_PAGINATED_WRAPPER = {
    'count': openapi.Schema(type=openapi.TYPE_INTEGER, description='Total record count'),
    'total_pages': openapi.Schema(type=openapi.TYPE_INTEGER),
    'current_page': openapi.Schema(type=openapi.TYPE_INTEGER),
    'next': openapi.Schema(type=openapi.TYPE_STRING, x_nullable=True),
    'previous': openapi.Schema(type=openapi.TYPE_STRING, x_nullable=True),
}


def _envelope(data_schema: openapi.Schema) -> openapi.Schema:
    """Wrap a data schema in the standard success envelope."""
    return openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'success': openapi.Schema(type=openapi.TYPE_BOOLEAN),
            'message': openapi.Schema(type=openapi.TYPE_STRING),
            'data': data_schema,
        },
    )


def _paginated_envelope(item_schema: openapi.Schema) -> openapi.Schema:
    """Wrap a list schema in the paginated success envelope."""
    return _envelope(
        openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                **_PAGINATED_WRAPPER,
                'results': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=item_schema,
                ),
            },
        )
    )


# ─── Master entity schema factories ───────────────────────────────────────────

def master_item_schema(entity: str) -> openapi.Schema:
    """Single master entity data schema."""
    return openapi.Schema(
        type=openapi.TYPE_OBJECT,
        title=entity,
        properties=_MASTER_PROPERTIES,
    )


def master_single_response(entity: str, description: str = '') -> openapi.Response:
    return openapi.Response(
        description=description or f'{entity} object',
        schema=_envelope(master_item_schema(entity)),
    )


def master_list_response(entity: str) -> openapi.Response:
    return openapi.Response(
        description=f'Paginated list of {entity}s',
        schema=_paginated_envelope(master_item_schema(entity)),
    )


def master_request_schema(entity: str) -> openapi.Schema:
    return openapi.Schema(
        type=openapi.TYPE_OBJECT,
        title=f'{entity} request',
        required=['name', 'code'],
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Human-readable label'),
            'code': openapi.Schema(type=openapi.TYPE_STRING, description='Unique machine identifier (auto-uppercased)'),
            'description': openapi.Schema(type=openapi.TYPE_STRING, default=''),
            'is_active': openapi.Schema(type=openapi.TYPE_BOOLEAN, default=True),
        },
    )


# ─── Mapping entity schema factories ──────────────────────────────────────────

def mapping_item_schema(parent_label: str, child_label: str) -> openapi.Schema:
    """Single mapping entity data schema with inline nested detail."""
    return openapi.Schema(
        type=openapi.TYPE_OBJECT,
        title=f'{parent_label}-{child_label} Mapping',
        properties={
            **_MAPPING_BASE_PROPERTIES,
            parent_label.lower(): openapi.Schema(
                type=openapi.TYPE_INTEGER, description=f'{parent_label} ID'
            ),
            f'{parent_label.lower()}_detail': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description=f'Nested {parent_label} object (read-only)',
                properties=_MASTER_PROPERTIES,
            ),
            child_label.lower(): openapi.Schema(
                type=openapi.TYPE_INTEGER, description=f'{child_label} ID'
            ),
            f'{child_label.lower()}_detail': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description=f'Nested {child_label} object (read-only)',
                properties=_MASTER_PROPERTIES,
            ),
        },
    )


def mapping_single_response(parent_label: str, child_label: str) -> openapi.Response:
    return openapi.Response(
        description=f'{parent_label}-{child_label} Mapping object',
        schema=_envelope(mapping_item_schema(parent_label, child_label)),
    )


def mapping_list_response(parent_label: str, child_label: str) -> openapi.Response:
    return openapi.Response(
        description=f'Paginated list of {parent_label}-{child_label} Mappings',
        schema=_paginated_envelope(mapping_item_schema(parent_label, child_label)),
    )


def mapping_request_schema(parent_label: str, child_label: str) -> openapi.Schema:
    return openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=[parent_label.lower(), child_label.lower()],
        properties={
            parent_label.lower(): openapi.Schema(
                type=openapi.TYPE_INTEGER, description=f'{parent_label} ID'
            ),
            child_label.lower(): openapi.Schema(
                type=openapi.TYPE_INTEGER, description=f'{child_label} ID'
            ),
            'primary_mapping': openapi.Schema(
                type=openapi.TYPE_BOOLEAN,
                default=False,
                description=f'Mark as primary {child_label} for this {parent_label} (only one allowed)',
            ),
            'is_active': openapi.Schema(type=openapi.TYPE_BOOLEAN, default=True),
        },
    )


# ─── Common query parameter definitions ────────────────────────────────────────

PARAM_IS_ACTIVE = openapi.Parameter(
    'is_active', openapi.IN_QUERY,
    description='Filter by active status',
    type=openapi.TYPE_BOOLEAN,
    required=False,
)

PARAM_PAGE = openapi.Parameter(
    'page', openapi.IN_QUERY,
    description='Page number (1-indexed)',
    type=openapi.TYPE_INTEGER,
    required=False,
)

PARAM_PAGE_SIZE = openapi.Parameter(
    'page_size', openapi.IN_QUERY,
    description='Results per page (max 100)',
    type=openapi.TYPE_INTEGER,
    required=False,
)

PARAM_PRIMARY_MAPPING = openapi.Parameter(
    'primary_mapping', openapi.IN_QUERY,
    description='Filter by primary mapping flag',
    type=openapi.TYPE_BOOLEAN,
    required=False,
)


def id_filter_param(entity: str) -> openapi.Parameter:
    """e.g. id_filter_param('vendor') → ?vendor_id=<int>"""
    return openapi.Parameter(
        f'{entity.lower()}_id', openapi.IN_QUERY,
        description=f'Filter by {entity} ID',
        type=openapi.TYPE_INTEGER,
        required=False,
    )


COMMON_LIST_PARAMS = [PARAM_IS_ACTIVE, PARAM_PAGE, PARAM_PAGE_SIZE]
MAPPING_LIST_PARAMS = [PARAM_IS_ACTIVE, PARAM_PRIMARY_MAPPING, PARAM_PAGE, PARAM_PAGE_SIZE]
