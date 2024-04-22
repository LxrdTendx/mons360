from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import License, Statistics, Product
from django.utils.timezone import now
from .serializers import StatisticsSerializer, LicenseSerializer, ProductSerializer
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.db.models import Q
from django.http import FileResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.utils.timezone import make_naive
import pandas as pd
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Statistics
import pytz


def download_statistics(request):
    if not request.user.is_authenticated:
        return redirect('login')

    timezone = pytz.timezone(settings.TIME_ZONE)  # Создание объекта временной зоны

    data = []
    for stat in Statistics.objects.filter(login_user=request.user.username):
        stat_dict = {
            'full_name': stat.full_name,
            'date': make_naive(stat.date, timezone) if stat.date else None,  # Исправление здесь
            'time': stat.time,
            'respirator_provided': 'Да' if stat.respirator_provided else 'Нет',
            'headlamp_provided': 'Да' if stat.headlamp_provided else 'Нет',
            'respirator_used': 'Да' if stat.respirator_used else 'Нет',
            'phone_message': 'Да' if stat.phone_message else 'Нет',
            'login_user': stat.login_user,
            'mission_complete': 'Да' if stat.mission_complete else 'Нет'
        }
        data.append(stat_dict)

    df = pd.DataFrame(data)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename="statistics.xlsx"'

    with pd.ExcelWriter(response, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Статистика')

    return response


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('user-statistics')  # Перенаправление на страницу со статистикой
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def user_statistics(request):
    if not request.user.is_authenticated:
        return redirect('login')
    stats = Statistics.objects.filter(login_user=request.user.username)
    return render(request, 'user_statistics.html', {'statistics': stats})



class ProductFileDownload(APIView):
    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        product = get_object_or_404(Product, pk=product_id)
        if product.url:
            return Response({"url": product.url})
        else:
            return Response({"message": "URL not found"}, status=status.HTTP_404_NOT_FOUND)


class LicenseCheck(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        product_id = request.data.get('product_id')
        user = authenticate(username=username, password=password)
        if user is not None:
            product = get_object_or_404(Product, pk=product_id)
            # Фильтрация лицензий, чтобы убедиться, что они активны и их срок действия не истёк
            licenses = License.objects.filter(
                user=user,
                product=product,
                is_active=True
            ).filter(
                # Лицензии, которые либо бессрочные, либо с непросроченным сроком действия
                Q(license_type='unlimited') | Q(expiry_date__gte=now().date())
            ).first()

            if licenses:
                return Response({"message": "License valid", "license_key": licenses.license_key, "type": licenses.license_type})
            else:
                return Response({"message": "License not found or expired"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Authentication failed"}, status=status.HTTP_401_UNAUTHORIZED)



class StatisticsView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = StatisticsSerializer(data=request.data)
        if serializer.is_valid():
            # Здесь предполагается, что в request.data уже есть 'product' с идентификатором продукта
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProductsView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            # Фильтруем лицензии, которые активны и у которых дата окончания либо в будущем, либо null
            licenses = License.objects.filter(user=user, is_active=True).exclude(expiry_date__lt=now().date())
            # Извлекаем уникальные продукты из этих лицензий
            products = Product.objects.filter(licenses__in=licenses).distinct()
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        else:
            return Response({"message": "Authentication failed"}, status=status.HTTP_401_UNAUTHORIZED)