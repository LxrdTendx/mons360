from django.contrib import admin
from django.urls import path, include  # Импортируйте include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('monsapp.urls')),  # Включите URL-адреса из myapp
]
