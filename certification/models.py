from core.models import MasterModel


class Certification(MasterModel):
    class Meta(MasterModel.Meta):
        verbose_name = 'Certification'
        verbose_name_plural = 'Certifications'
        db_table = 'certification'
