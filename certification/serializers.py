from core.serializers import BaseMasterSerializer
from .models import Certification


class CertificationSerializer(BaseMasterSerializer):
    class Meta(BaseMasterSerializer.Meta):
        model = Certification
