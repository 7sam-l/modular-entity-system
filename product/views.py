"""
Product views — list/create and retrieve/update/delete.
"""
import logging
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from core.mixins import MasterEntityMixin
from core.swagger import (
    master_single_response, master_list_response,
    master_request_schema, COMMON_LIST_PARAMS, id_filter_param,
)
from vendor_product_mapping.models import VendorProductMapping
from .models import Product
from .serializers import ProductSerializer

logger = logging.getLogger('app')
_TAG = ['Products']


class ProductListView(MasterEntityMixin, APIView):
    model = Product
    serializer_class = ProductSerializer
    entity_label = 'Product'
    child_id_param = 'vendor_id'
    child_mapping_model = VendorProductMapping
    child_mapping_field = 'product_id'

    @swagger_auto_schema(
        operation_summary='List all Products',
        operation_description='Filter by `vendor_id` to get Products linked to a specific parent entity.',
        manual_parameters=COMMON_LIST_PARAMS + [id_filter_param('vendor')],
        responses={200: master_list_response('Product')},
        tags=_TAG,
    )
    def get(self, request: Request) -> Response:
        return self.list(request)

    @swagger_auto_schema(
        operation_summary='Create a Product',
        request_body=master_request_schema('Product'),
        responses={201: master_single_response('Product'), 400: 'Validation error'},
        tags=_TAG,
    )
    def post(self, request: Request) -> Response:
        return self.create(request)


class ProductDetailView(MasterEntityMixin, APIView):
    model = Product
    serializer_class = ProductSerializer
    entity_label = 'Product'

    @swagger_auto_schema(
        operation_summary='Retrieve a Product',
        responses={200: master_single_response('Product'), 404: 'Not found'},
        tags=_TAG,
    )
    def get(self, request: Request, pk: int) -> Response:
        return self.retrieve(request, pk)

    @swagger_auto_schema(
        operation_summary='Full update a Product',
        request_body=master_request_schema('Product'),
        responses={200: master_single_response('Product'), 400: 'Validation error', 404: 'Not found'},
        tags=_TAG,
    )
    def put(self, request: Request, pk: int) -> Response:
        return self.update(request, pk)

    @swagger_auto_schema(
        operation_summary='Partial update a Product',
        request_body=master_request_schema('Product'),
        responses={200: master_single_response('Product'), 400: 'Validation error', 404: 'Not found'},
        tags=_TAG,
    )
    def patch(self, request: Request, pk: int) -> Response:
        return self.update(request, pk, partial=True)

    @swagger_auto_schema(
        operation_summary='Soft-delete a Product',
        operation_description='Marks the record as inactive. Data is preserved in the database.',
        responses={204: 'Soft-deleted', 404: 'Not found'},
        tags=_TAG,
    )
    def delete(self, request: Request, pk: int) -> Response:
        return self.destroy(request, pk)
