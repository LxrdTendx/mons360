from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import License
from django.utils.timezone import now

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
