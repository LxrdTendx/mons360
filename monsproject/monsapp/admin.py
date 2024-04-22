from django.contrib import admin
from django.contrib.auth.models import User
from .models import License, Statistics, Product

class LicenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'license_type', 'license_key', 'expiry_date', 'is_active')
    list_filter = ('license_type', 'product', 'is_active')
    search_fields = ('user__username', 'license_key')

class StatisticsAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'login_user','date', 'time', 'respirator_provided', 'headlamp_provided', 'respirator_used', 'phone_message', 'mission_complete')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'release_date', 'url')  # Отображаемые поля в списке
    search_fields = ('name',)  # Поля, по которым можно осуществлять поиск

admin.site.register(Product, ProductAdmin)
admin.site.register(Statistics, StatisticsAdmin)
admin.site.register(License, LicenseAdmin)
