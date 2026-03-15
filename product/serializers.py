from core.serializers import BaseMasterSerializer
from .models import Product


class ProductSerializer(BaseMasterSerializer):
    class Meta(BaseMasterSerializer.Meta):
        model = Product
