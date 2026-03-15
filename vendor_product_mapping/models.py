from django.db import models
from core.models import MappingModel
from vendor.models import Vendor
from product.models import Product


class VendorProductMapping(MappingModel):
    """
    Maps Vendor → Product.

    Constraints:
      - The (vendor, product) pair is unique (enforced at DB + serializer level).
      - Only one mapping per Vendor may have primary_mapping=True.
    """

    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.PROTECT,
        related_name='vendor_product_mappings',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='vendor_product_mappings',
    )

    class Meta(MappingModel.Meta):
        verbose_name = 'Vendor-Product Mapping'
        verbose_name_plural = 'Vendor-Product Mappings'
        db_table = 'vendor_product_mapping'
        unique_together = [('vendor', 'product')]
        indexes = [
            models.Index(fields=['vendor', 'is_active'], name='vpm_vendor_active_idx'),
            models.Index(fields=['product', 'is_active'], name='vpm_product_active_idx'),
        ]

    def __str__(self) -> str:
        return f'Vendor({self.vendor_id}) -> Product({self.product_id})'
