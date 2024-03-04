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

class ProductFileDownload(APIView):
    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        product = get_object_or_404(Product, pk=product_id)
        if product.file:
            return FileResponse(product.file.open(), as_attachment=True, filename=product.file.name)
        else:
            return Response({"message": "File not found"}, status=status.HTTP_404_NOT_FOUND)


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