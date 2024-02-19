from django.contrib import admin
from django.contrib.auth.models import User
from .models import License, Statistics

class LicenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'license_key', 'expiry_date', 'is_active')

class StatisticsAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'date', 'time', 'respirator_provided', 'headlamp_provided', 'respirator_used', 'phone_message')


admin.site.register(Statistics, StatisticsAdmin)
admin.site.register(License, LicenseAdmin)
