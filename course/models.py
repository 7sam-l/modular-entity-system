from core.models import MasterModel


class Course(MasterModel):
    class Meta(MasterModel.Meta):
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
        db_table = 'course'
