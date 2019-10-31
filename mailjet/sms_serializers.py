from rest_framework import serializers
from drf_yasg.utils import swagger_serializer_method
from .models import *

class SendSmsSerializer(serializers.Serializer):
    to_telnumber = serializers.CharField(required=True)

class SendSmsResponseSerializer(serializers.Serializer):
    From = serializers.CharField(required=False)
    To = serializers.CharField(required=False)
    Text = serializers.CharField(required=False)
    MessageId = serializers.CharField(required=False)
    SmsCount = serializers.IntegerField(required=False)
    CreationTS = serializers.CharField(required=False)
    SentTS = serializers.CharField(required=False)
    Cost = serializers.JSONField(required=False)
    Status = serializers.JSONField(required=False)
