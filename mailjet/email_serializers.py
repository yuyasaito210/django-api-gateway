from rest_framework import serializers
from drf_yasg.utils import swagger_serializer_method
from .models import *

class SendEmailSerializer(serializers.Serializer):
    to_email = serializers.CharField(required=False)
    to_name = serializers.CharField(required=False)

class SendEmailResponseSerializer(serializers.Serializer):
    start_date = serializers.CharField(required=False)
    end_date = serializers.CharField(required=False)
