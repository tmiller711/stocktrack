from django.urls import path

from .views import RegisterAccount, LoginAccount, GetAccount

urlpatterns = [
    path('register', RegisterAccount.as_view()),
    path('login', LoginAccount.as_view()),
    path('getaccount', GetAccount.as_view()),
]
