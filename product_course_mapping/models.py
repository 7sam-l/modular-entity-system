from django.db import models
from core.models import MappingModel
from product.models import Product
from course.models import Course


class ProductCourseMapping(MappingModel):
    """
    Maps Product → Course.

    Constraints:
      - The (product, course) pair is unique (enforced at DB + serializer level).
      - Only one mapping per Product may have primary_mapping=True.
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='product_course_mappings',
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name='product_course_mappings',
    )

    class Meta(MappingModel.Meta):
        verbose_name = 'Product-Course Mapping'
        verbose_name_plural = 'Product-Course Mappings'
        db_table = 'product_course_mapping'
        unique_together = [('product', 'course')]
        indexes = [
            models.Index(fields=['product', 'is_active'], name='pcm_product_active_idx'),
            models.Index(fields=['course', 'is_active'], name='pcm_course_active_idx'),
        ]

    def __str__(self) -> str:
        return f'Product({self.product_id}) -> Course({self.course_id})'
