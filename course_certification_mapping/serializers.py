from core.serializers import BaseMappingSerializer
from course.models import Course
from course.serializers import CourseSerializer
from certification.models import Certification
from certification.serializers import CertificationSerializer
from .models import CourseCertificationMapping


class CourseCertificationMappingSerializer(BaseMappingSerializer):
    """
    Serializer for CourseCertificationMapping.
    Inherits duplicate-pair and primary_mapping validation from BaseMappingSerializer.
    """

    course_detail = CourseSerializer(source='course', read_only=True)
    certification_detail = CertificationSerializer(source='certification', read_only=True)

    _parent_field = 'course'
    _child_field = 'certification'
    _parent_model = Course
    _child_model = Certification

    class Meta(BaseMappingSerializer.Meta):
        model = CourseCertificationMapping
        fields = [
            'id',
            'course', 'course_detail',
            'certification', 'certification_detail',
            'primary_mapping', 'is_active',
            'created_at', 'updated_at',
        ]
        read_only_fields = BaseMappingSerializer.Meta.read_only_fields + [
            'course_detail', 'certification_detail',
        ]
