from django.urls import path
from .views import GetStockData

urlpatterns = [
    path('<str:tikr>/', GetStockData.as_view())
]
