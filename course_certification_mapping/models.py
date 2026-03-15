from django.db import models
from core.models import MappingModel
from course.models import Course
from certification.models import Certification


class CourseCertificationMapping(MappingModel):
    """
    Maps Course → Certification.

    Constraints:
      - The (course, certification) pair is unique (enforced at DB + serializer level).
      - Only one mapping per Course may have primary_mapping=True.
    """

    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name='course_certification_mappings',
    )
    certification = models.ForeignKey(
        Certification,
        on_delete=models.PROTECT,
        related_name='course_certification_mappings',
    )

    class Meta(MappingModel.Meta):
        verbose_name = 'Course-Certification Mapping'
        verbose_name_plural = 'Course-Certification Mappings'
        db_table = 'course_certification_mapping'
        unique_together = [('course', 'certification')]
        indexes = [
            models.Index(fields=['course', 'is_active'], name='ccm_course_active_idx'),
            models.Index(fields=['certification', 'is_active'], name='ccm_cert_active_idx'),
        ]

    def __str__(self) -> str:
        return f'Course({self.course_id}) -> Certification({self.certification_id})'
