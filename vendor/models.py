from core.models import MasterModel


class Vendor(MasterModel):
    class Meta(MasterModel.Meta):
        verbose_name = 'Vendor'
        verbose_name_plural = 'Vendors'
        db_table = 'vendor'
