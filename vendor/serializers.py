from core.serializers import BaseMasterSerializer
from .models import Vendor


class VendorSerializer(BaseMasterSerializer):
    class Meta(BaseMasterSerializer.Meta):
        model = Vendor
