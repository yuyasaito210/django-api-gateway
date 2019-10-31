from rest_framework import serializers
from drf_yasg.utils import swagger_serializer_method
from .models import *

class SendEmailSerializer(serializers.Serializer):
    to_email = serializers.CharField(required=True)
    to_name = serializers.CharField(required=True)

class SendEmailResponseSerializer(serializers.Serializer):
    status = serializers.IntegerField()
    message = serializers.ListField()
