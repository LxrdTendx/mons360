from rest_framework import serializers
from .models import License, Statistics

class LicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = License
        fields = ['user', 'license_key', 'expiry_date', 'is_active']

class StatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistics
        fields = ['full_name', 'date', 'time', 'respirator_provided', 'headlamp_provided', 'respirator_used']
