from rest_framework import serializers
from drf_yasg.utils import swagger_serializer_method
from .models import *

class SendSmsSerializer(serializers.Serializer):
    result = serializers.JSONField(binary=True, encoder=None, required=False)

class SendSmsResponseSerializer(serializers.Serializer):
    result = serializers.JSONField(binary=True, encoder=None, required=False)
