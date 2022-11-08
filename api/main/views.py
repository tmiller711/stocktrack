from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, date
import pandas as pd

from .models import Stock
from .serializers import StockSerializer

# Create your views here.

class GetStockData(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        indicator_args = request.data.get('indicators')
        start_date = datetime.strptime(request.data.get('start_date'), "%Y-%m-%d").date()
        end_date = datetime.strptime(request.data.get('end_date'), "%Y-%m-%d").date()
        
        ticker = kwargs['tikr']
        try:
            stock = Stock.objects.get(ticker=ticker)
        except:
            return Response({"Error": "Stock not found"}, status=status.HTTP_404_NOT_FOUND)

        data = pd.read_csv(stock.stock_data)
        for index, row in data.iterrows():
            # convert timestamp to date format
            data.at[index, 'time'] = date.fromtimestamp(row['time'])

        data = data[(data['time'] >= start_date) & (data['time'] <= end_date)]

        indicators = ['time', 'open', 'close', 'high', 'low']
        for indicator in indicator_args:
            indicators.append(indicator)
        data = data[indicators]

        return Response(data, status=status.HTTP_200_OK)
