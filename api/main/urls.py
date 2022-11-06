from django.urls import path
from .views import GetStockData

urlpatterns = [
    path('api/<str:tikr>', GetStockData.as_view())
]
