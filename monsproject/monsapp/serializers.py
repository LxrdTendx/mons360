from rest_framework import serializers
from .models import License

class LicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = License
        fields = ['user', 'license_key', 'expiry_date', 'is_active']
