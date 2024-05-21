from django.urls import path
from .views import LicenseCheck, StatisticsView, UserProductsView, ProductFileDownload, user_login, download_statistics, user_statistics, AnatolyStatisticsView, anatoly_statistics_list
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('api/check-license/', LicenseCheck.as_view(), name='check-license'),
    path('api/statistics/', StatisticsView.as_view(), name='statistics'),
    path('api/user-products/', UserProductsView.as_view(), name='user-products'),
    path('api/products/<int:product_id>/download/', ProductFileDownload.as_view(), name='product-download'),
    path('', user_login, name='login'),
    path('statistics/', user_statistics, name='user-statistics'),
    path('download-statistics/', download_statistics, name='download_statistics'),


    #Толины ручки для статистики
    path('anatoly-statistics/', anatoly_statistics_list, name='anatoly_statistics_list'),
    path('api/anatoly-statistics/', AnatolyStatisticsView.as_view(), name='anatoly_statistics_api'),
    path('api/anatoly-statistics/top/', AnatolyStatisticsView.as_view(), name='anatoly_statistics_top'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

