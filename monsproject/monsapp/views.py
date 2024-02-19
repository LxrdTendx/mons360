from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import License, Statistics
from django.utils.timezone import now
from .serializers import StatisticsSerializer

class LicenseCheck(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            try:
                license = License.objects.get(user=user, is_active=True, expiry_date__gte=now().date())
                return Response({"message": "License valid", "license_key": license.license_key})
            except License.DoesNotExist:
                return Response({"message": "License not found or expired"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Authentication failed bruh"}, status=status.HTTP_401_UNAUTHORIZED)



class StatisticsView(APIView):
    def get(self, request, *args, **kwargs):
        stats = Statistics.objects.all()
        serializer = StatisticsSerializer(stats, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = StatisticsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
