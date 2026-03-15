"""
Base APIView mixins — the single biggest DRY win in this refactor.

Before: each of 7 views.py had 120–180 lines of near-identical CRUD code.
After:  each views.py is 30–40 lines; only the entity-specific bindings differ.

MasterEntityMixin   → used by Vendor, Product, Course, Certification
MappingEntityMixin  → used by VendorProductMapping, ProductCourseMapping,
                                CourseCertificationMapping

The mixin provides:
  list()         — GET /entities/
  create()       — POST /entities/
  retrieve()     — GET /entities/<pk>/
  update()       — PUT  /entities/<pk>/
  partial_update() — PATCH /entities/<pk>/
  destroy()      — DELETE /entities/<pk>/

Subclasses bind:
  model           — Django model class
  serializer_class — serializer for the model
  entity_label    — human-readable name used in response messages (e.g. "Vendor")
"""

import logging
from typing import Any

from rest_framework.request import Request
from rest_framework.response import Response

from .filters import filter_is_active, filter_by_int_param, filter_primary_mapping
from .helpers import (
    get_object_or_error,
    success_response,
    created_response,
    no_content_response,
    validation_error_response,
)
from .pagination import StandardResultsPagination

logger = logging.getLogger('app')


# ─── Master entity mixin ───────────────────────────────────────────────────────

class MasterEntityMixin:
    """
    Provides CRUD logic for master entity views (Vendor, Product, Course, Certification).

    Class attributes to set in the concrete view:
        model             — model class
        serializer_class  — serializer class
        entity_label      — e.g. "Vendor"
        child_id_param    — optional query param name for cross-entity filtering
                            e.g. 'vendor_id' on ProductListCreateView
        child_mapping_model — optional mapping model used for the above filter
        child_mapping_field — FK field name in the mapping model, e.g. 'product_id'
    """

    model = None
    serializer_class = None
    entity_label: str = ''
    child_id_param: str | None = None        # e.g. 'vendor_id'
    child_mapping_model = None               # e.g. VendorProductMapping
    child_mapping_field: str | None = None   # e.g. 'product_id'

    # ── List ──────────────────────────────────────────────────────────────────

    def list(self, request: Request) -> Response:
        queryset = self.model.objects.all()

        # Cross-entity filter (e.g. products for a specific vendor)
        if self.child_id_param and self.child_mapping_model and self.child_mapping_field:
            queryset, err = self._apply_parent_filter(request, queryset)
            if err:
                return err

        # is_active filter
        queryset, err = filter_is_active(queryset, request)
        if err:
            return err

        # Paginate
        paginator = StandardResultsPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def _apply_parent_filter(self, request: Request, queryset: Any):
        raw = request.query_params.get(self.child_id_param)
        if raw is None:
            return queryset, None
        try:
            parent_id = int(raw)
        except (ValueError, TypeError):
            from .helpers import error_response
            return None, error_response(
                message=f'Query param "{self.child_id_param}" must be a positive integer.'
            )
        child_ids = self.child_mapping_model.objects.filter(
            **{self.child_id_param: parent_id, 'is_active': True}
        ).values_list(self.child_mapping_field, flat=True)
        return queryset.filter(id__in=child_ids), None

    # ── Create ────────────────────────────────────────────────────────────────

    def create(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            logger.info('%s created: pk=%s code=%s', self.entity_label, instance.pk,
                        getattr(instance, 'code', ''))
            return created_response(
                self.serializer_class(instance).data,
                message=f'{self.entity_label} created successfully.',
            )
        return validation_error_response(self.entity_label, serializer.errors)

    # ── Retrieve ──────────────────────────────────────────────────────────────

    def retrieve(self, request: Request, pk: Any) -> Response:
        instance, err = get_object_or_error(self.model, pk)
        if err:
            return err
        return success_response(
            self.serializer_class(instance).data,
            message=f'{self.entity_label} retrieved successfully.',
        )

    # ── Update (full) ─────────────────────────────────────────────────────────

    def update(self, request: Request, pk: Any, partial: bool = False) -> Response:
        instance, err = get_object_or_error(self.model, pk)
        if err:
            return err
        serializer = self.serializer_class(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            updated = serializer.save()
            verb = 'partially updated' if partial else 'updated'
            logger.info('%s %s: pk=%s', self.entity_label, verb, updated.pk)
            return success_response(
                self.serializer_class(updated).data,
                message=f'{self.entity_label} {verb} successfully.',
            )
        return validation_error_response(self.entity_label, serializer.errors)

    # ── Destroy (soft delete) ─────────────────────────────────────────────────

    def destroy(self, request: Request, pk: Any) -> Response:
        instance, err = get_object_or_error(self.model, pk)
        if err:
            return err
        instance.soft_delete()
        logger.info('%s soft-deleted: pk=%s', self.entity_label, pk)
        return no_content_response(f'{self.entity_label} soft-deleted successfully.')


# ─── Mapping entity mixin ──────────────────────────────────────────────────────

class MappingEntityMixin:
    """
    Provides CRUD logic for mapping entity views.

    Class attributes to set in the concrete view:
        model             — mapping model class
        serializer_class  — serializer class
        entity_label      — e.g. "Vendor-Product Mapping"
        parent_id_param   — query param name, e.g. 'vendor_id'
        child_id_param    — query param name, e.g. 'product_id'
    """

    model = None
    serializer_class = None
    entity_label: str = ''
    parent_id_param: str = ''
    child_id_param: str = ''

    # ── List ──────────────────────────────────────────────────────────────────

    def list(self, request: Request) -> Response:
        queryset = self.model.objects.select_related().all()

        # Parent FK filter (e.g. ?vendor_id=1)
        if self.parent_id_param:
            queryset, err = filter_by_int_param(
                queryset, request, self.parent_id_param, self.parent_id_param
            )
            if err:
                return err

        # Child FK filter (e.g. ?product_id=2)
        if self.child_id_param:
            queryset, err = filter_by_int_param(
                queryset, request, self.child_id_param, self.child_id_param
            )
            if err:
                return err

        # primary_mapping filter
        queryset, err = filter_primary_mapping(queryset, request)
        if err:
            return err

        # is_active filter
        queryset, err = filter_is_active(queryset, request)
        if err:
            return err

        paginator = StandardResultsPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    # ── Create ────────────────────────────────────────────────────────────────

    def create(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            logger.info('%s created: pk=%s', self.entity_label, instance.pk)
            return created_response(
                self.serializer_class(instance).data,
                message=f'{self.entity_label} created successfully.',
            )
        return validation_error_response(self.entity_label, serializer.errors)

    # ── Retrieve ──────────────────────────────────────────────────────────────

    def retrieve(self, request: Request, pk: Any) -> Response:
        instance, err = get_object_or_error(self.model, pk)
        if err:
            return err
        return success_response(
            self.serializer_class(instance).data,
            message=f'{self.entity_label} retrieved successfully.',
        )

    # ── Update ────────────────────────────────────────────────────────────────

    def update(self, request: Request, pk: Any, partial: bool = False) -> Response:
        instance, err = get_object_or_error(self.model, pk)
        if err:
            return err
        serializer = self.serializer_class(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            updated = serializer.save()
            verb = 'partially updated' if partial else 'updated'
            logger.info('%s %s: pk=%s', self.entity_label, verb, updated.pk)
            return success_response(
                self.serializer_class(updated).data,
                message=f'{self.entity_label} {verb} successfully.',
            )
        return validation_error_response(self.entity_label, serializer.errors)

    # ── Destroy ───────────────────────────────────────────────────────────────

    def destroy(self, request: Request, pk: Any) -> Response:
        instance, err = get_object_or_error(self.model, pk)
        if err:
            return err
        instance.soft_delete()
        logger.info('%s soft-deleted: pk=%s', self.entity_label, pk)
        return no_content_response(f'{self.entity_label} soft-deleted successfully.')
