from django.urls import path
from .views import LicenseCheck, StatisticsView, UserProductsView, ProductFileDownload
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('api/check-license/', LicenseCheck.as_view(), name='check-license'),
    path('api/statistics/', StatisticsView.as_view(), name='statistics'),
    path('api/user-products/', UserProductsView.as_view(), name='user-products'),
    path('api/products/<int:product_id>/download/', ProductFileDownload.as_view(), name='product-download'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

