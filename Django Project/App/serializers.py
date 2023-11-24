from rest_framework import serializers
from .models import Vendor, PurchaseOrder # Assuming your model is in models.py within the same app

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor  # Corrected typo: 'Vendor' instead of 'Vender'
        fields = '__all__'


class PurchaseOrderSerializers(serializers.ModelSerializer):
    class Meta:
        model=PurchaseOrder
        fields = '__all__'