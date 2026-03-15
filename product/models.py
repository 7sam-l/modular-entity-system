from core.models import MasterModel


class Product(MasterModel):
    class Meta(MasterModel.Meta):
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        db_table = 'product'
