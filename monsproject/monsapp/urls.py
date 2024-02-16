from django.urls import path
from .views import LicenseCheck

urlpatterns = [
    path('api/check-license/', LicenseCheck.as_view(), name='check-license'),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
