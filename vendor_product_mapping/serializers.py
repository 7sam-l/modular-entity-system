from core.serializers import BaseMappingSerializer
from vendor.models import Vendor
from vendor.serializers import VendorSerializer
from product.models import Product
from product.serializers import ProductSerializer
from .models import VendorProductMapping


class VendorProductMappingSerializer(BaseMappingSerializer):
    """
    Serializer for VendorProductMapping.
    Inherits duplicate-pair and primary_mapping validation from BaseMappingSerializer.
    """

    vendor_detail = VendorSerializer(source='vendor', read_only=True)
    product_detail = ProductSerializer(source='product', read_only=True)

    _parent_field = 'vendor'
    _child_field = 'product'
    _parent_model = Vendor
    _child_model = Product

    class Meta(BaseMappingSerializer.Meta):
        model = VendorProductMapping
        fields = [
            'id',
            'vendor', 'vendor_detail',
            'product', 'product_detail',
            'primary_mapping', 'is_active',
            'created_at', 'updated_at',
        ]
        read_only_fields = BaseMappingSerializer.Meta.read_only_fields + [
            'vendor_detail', 'product_detail',
        ]
