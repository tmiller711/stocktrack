from rest_framework import serializers
from .models import Account
from django.contrib.auth import get_user_model

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'password')
