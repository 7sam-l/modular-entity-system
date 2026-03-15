"""
VendorProductMapping views.
"""
import logging
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from core.mixins import MappingEntityMixin
from core.swagger import (
    mapping_single_response, mapping_list_response,
    mapping_request_schema, MAPPING_LIST_PARAMS, id_filter_param,
)
from .models import VendorProductMapping
from .serializers import VendorProductMappingSerializer

logger = logging.getLogger('app')
_TAG = ['Vendor-Product Mappings']
_PARENT = 'Vendor'
_CHILD = 'Product'


class VendorProductMappingListView(MappingEntityMixin, APIView):
    model = VendorProductMapping
    serializer_class = VendorProductMappingSerializer
    entity_label = 'Vendor-Product Mapping'
    parent_id_param = 'vendor_id'
    child_id_param = 'product_id'

    @swagger_auto_schema(
        operation_summary='List all Vendor-Product Mappings',
        manual_parameters=MAPPING_LIST_PARAMS + [
            id_filter_param(_PARENT), id_filter_param(_CHILD),
        ],
        responses={200: mapping_list_response(_PARENT, _CHILD)},
        tags=_TAG,
    )
    def get(self, request: Request) -> Response:
        return self.list(request)

    @swagger_auto_schema(
        operation_summary='Create a Vendor-Product Mapping',
        operation_description=(
            'Links a Vendor to a Product.\n\n'
            '**Constraints:**\n'
            '- The (vendor, product) pair must be unique.\n'
            '- Only one mapping per Vendor can have `primary_mapping=True`.'
        ),
        request_body=mapping_request_schema(_PARENT, _CHILD),
        responses={201: mapping_single_response(_PARENT, _CHILD), 400: 'Validation error'},
        tags=_TAG,
    )
    def post(self, request: Request) -> Response:
        return self.create(request)


class VendorProductMappingDetailView(MappingEntityMixin, APIView):
    model = VendorProductMapping
    serializer_class = VendorProductMappingSerializer
    entity_label = 'Vendor-Product Mapping'
    parent_id_param = 'vendor_id'
    child_id_param = 'product_id'

    @swagger_auto_schema(
        operation_summary='Retrieve a Vendor-Product Mapping',
        responses={200: mapping_single_response(_PARENT, _CHILD), 404: 'Not found'},
        tags=_TAG,
    )
    def get(self, request: Request, pk: int) -> Response:
        return self.retrieve(request, pk)

    @swagger_auto_schema(
        operation_summary='Full update a Vendor-Product Mapping',
        request_body=mapping_request_schema(_PARENT, _CHILD),
        responses={200: mapping_single_response(_PARENT, _CHILD), 400: 'Validation error', 404: 'Not found'},
        tags=_TAG,
    )
    def put(self, request: Request, pk: int) -> Response:
        return self.update(request, pk)

    @swagger_auto_schema(
        operation_summary='Partial update a Vendor-Product Mapping',
        request_body=mapping_request_schema(_PARENT, _CHILD),
        responses={200: mapping_single_response(_PARENT, _CHILD), 400: 'Validation error', 404: 'Not found'},
        tags=_TAG,
    )
    def patch(self, request: Request, pk: int) -> Response:
        return self.update(request, pk, partial=True)

    @swagger_auto_schema(
        operation_summary='Soft-delete a Vendor-Product Mapping',
        responses={204: 'Soft-deleted', 404: 'Not found'},
        tags=_TAG,
    )
    def delete(self, request: Request, pk: int) -> Response:
        return self.destroy(request, pk)
