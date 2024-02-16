from django.urls import path
from .views import LicenseCheck

urlpatterns = [
    path('api/check-license/', LicenseCheck.as_view(), name='check-license'),
]
