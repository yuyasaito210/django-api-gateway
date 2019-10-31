from rest_framework import serializers
from drf_yasg.utils import swagger_serializer_method
from .models import *

class SendSmsSerializer(serializers.Serializer):
    to_telnumber = serializers.CharField(required=True)

class SendSmsResponseSerializer(serializers.Serializer):
    status = serializers.IntegerField()
    message = serializers.ListField()
