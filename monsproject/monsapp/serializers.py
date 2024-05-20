from rest_framework import serializers
from .models import License, Statistics, Product, AnatolyStatistics
from datetime import datetime, time

class LicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = License
        fields = ['user', 'license_key', 'expiry_date', 'is_active']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'version', 'release_date', 'url']

class StatisticsSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True)

    class Meta:
        model = Statistics
        fields = ['product', 'product_id', 'login_user','full_name', 'date', 'time', 'respirator_provided', 'headlamp_provided', 'respirator_used', 'phone_message', 'login_user', 'mission_complete']


class MinuteSecondTimeField(serializers.Field):
    def to_internal_value(self, data):
        try:
            # Expecting time format as MM:SS
            minutes, seconds = map(int, data.split(':'))
            return time(minute=minutes, second=seconds)
        except ValueError:
            raise serializers.ValidationError("Неправильный формат времени. Используйте формат MM:SS.")

    def to_representation(self, value):
        # Represent the time in MM:SS format
        return value.strftime('%M:%S')

class AnatolyStatisticsSerializer(serializers.ModelSerializer):
    time = MinuteSecondTimeField()

    class Meta:
        model = AnatolyStatistics
        fields = ['name', 'time']