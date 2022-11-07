from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
import pandas as pd

from .models import Stock
from .serializers import StockSerializer

# Create your views here.

class GetStockData(APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        indicator_args = request.data.get('indicators')
        ticker = kwargs['tikr']
        try:
            stock = Stock.objects.get(ticker=ticker)
        except:
            return Response({"Error": "Stock not found"}, status=status.HTTP_404_NOT_FOUND)

        data = pd.read_csv(stock.stock_data)
        indicators = ['time', 'open', 'close', 'high', 'low']
        for indicator in indicator_args:
            indicators.append(indicator)
        data = data[indicators]
        # print(data)

        return Response(data, status=status.HTTP_200_OK)
