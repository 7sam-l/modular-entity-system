"""
Shared constants used across the entire project.
"""

# ─── Validation ────────────────────────────────────────────────────────────────

CODE_MAX_LENGTH: int = 100
NAME_MAX_LENGTH: int = 255

# ─── Response messages ─────────────────────────────────────────────────────────

MSG_NOT_FOUND = '{entity} with id {pk} not found.'
MSG_CREATED = '{entity} created successfully.'
MSG_RETRIEVED = '{entity} retrieved successfully.'
MSG_LIST_RETRIEVED = '{entity} list retrieved successfully.'
MSG_UPDATED = '{entity} updated successfully.'
MSG_PARTIALLY_UPDATED = '{entity} partially updated successfully.'
MSG_DELETED = '{entity} soft-deleted successfully.'
MSG_VALIDATION_FAILED = '{entity} validation failed.'
MSG_DUPLICATE_MAPPING = 'A mapping between {parent}({parent_pk}) and {child}({child_pk}) already exists.'
MSG_DUPLICATE_PRIMARY = '{parent}({parent_pk}) already has a primary {child} mapping.'

# ─── Query param names ─────────────────────────────────────────────────────────

PARAM_IS_ACTIVE = 'is_active'
PARAM_PAGE = 'page'
PARAM_PAGE_SIZE = 'page_size'
PARAM_VENDOR_ID = 'vendor_id'
PARAM_PRODUCT_ID = 'product_id'
PARAM_COURSE_ID = 'course_id'
PARAM_CERTIFICATION_ID = 'certification_id'
PARAM_PRIMARY_MAPPING = 'primary_mapping'
