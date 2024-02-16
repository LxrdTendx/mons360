from django.urls import path
from .views import LicenseCheck
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('api/check-license/', LicenseCheck.as_view(), name='check-license'),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
