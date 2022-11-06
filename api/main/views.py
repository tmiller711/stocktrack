from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView

# Create your views here.

class GetStockData(APIView):
    def post(self, request, *args, **kwargs):
        tikr = self.kwargs['tikr']
