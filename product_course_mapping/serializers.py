from core.serializers import BaseMappingSerializer
from product.models import Product
from product.serializers import ProductSerializer
from course.models import Course
from course.serializers import CourseSerializer
from .models import ProductCourseMapping


class ProductCourseMappingSerializer(BaseMappingSerializer):
    """
    Serializer for ProductCourseMapping.
    Inherits duplicate-pair and primary_mapping validation from BaseMappingSerializer.
    """

    product_detail = ProductSerializer(source='product', read_only=True)
    course_detail = CourseSerializer(source='course', read_only=True)

    _parent_field = 'product'
    _child_field = 'course'
    _parent_model = Product
    _child_model = Course

    class Meta(BaseMappingSerializer.Meta):
        model = ProductCourseMapping
        fields = [
            'id',
            'product', 'product_detail',
            'course', 'course_detail',
            'primary_mapping', 'is_active',
            'created_at', 'updated_at',
        ]
        read_only_fields = BaseMappingSerializer.Meta.read_only_fields + [
            'product_detail', 'course_detail',
        ]
