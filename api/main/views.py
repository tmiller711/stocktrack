from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
import pandas as pd

from .models import Stock
from .serializers import StockSerializer

# Create your views here.

class GetStockData(APIView):
    def get(self, request, *args, **kwargs):
        ticker = kwargs['tikr']
        try:
            stock = Stock.objects.get(ticker=ticker)
        except:
            return Response({"Error": "Stock not found"}, status=status.HTTP_404_NOT_FOUND)

        data = pd.read_csv(stock.stock_data)
        print(data)
        print(request.data)
        return Response()
