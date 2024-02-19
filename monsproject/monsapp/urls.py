from django.urls import path
from .views import LicenseCheck, StatisticsView
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('api/check-license/', LicenseCheck.as_view(), name='check-license'),
    path('api/statistics/', StatisticsView.as_view(), name='statistics'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

