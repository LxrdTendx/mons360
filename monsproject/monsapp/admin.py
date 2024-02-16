from django.contrib import admin
from django.contrib.auth.models import User
from .models import License

class LicenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'license_key', 'expiry_date', 'is_active')

admin.site.register(License, LicenseAdmin)
