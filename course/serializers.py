from core.serializers import BaseMasterSerializer
from .models import Course


class CourseSerializer(BaseMasterSerializer):
    class Meta(BaseMasterSerializer.Meta):
        model = Course
