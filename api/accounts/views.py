from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login, authenticate
from rest_framework.permissions import IsAuthenticated

from .serializers import AccountSerializer
from .models import Account

# Create your views here.
class RegisterAccount(APIView):
    def post(self, request, format=None):
        print(request.data)
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')

            account = Account(email=email)
            account.set_password(password)
            account.save()
            print(serializer.data)
            return Response({'Account created': 'Good stuff'}, status=status.HTTP_201_CREATED)

        return Response({'error': 'creating account'}, status=status.HTTP_400_BAD_REQUEST)

class LoginAccount(APIView):
    def post(self, request, format=None):
            email = request.data.get('email')
            password = request.data.get('password')
            if len(email) > 0 and len(password) > 0:
                account = authenticate(request, email=email, password=password)
                if account is not None:
                    login(request, account)
                    return Response({'Logged': 'In'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'signing in'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'error': 'signing in'}, status=status.HTTP_400_BAD_REQUEST)

class GetAccount(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        account = Account(email=request.user.email)
        if account is not None:
            return Response({'email': account.email}, status=status.HTTP_200_OK)
        return Response({"error": "couldn't find account"}, status=status.HTTP_404_NOT_FOUND)
