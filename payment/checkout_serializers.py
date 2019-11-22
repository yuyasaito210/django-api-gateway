from rest_framework import serializers
from drf_yasg.utils import swagger_serializer_method
from .models import *

class CheckoutSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    telnumber = serializers.CharField(required=True)
    stationSn = serializers.CharField(required=True)
    slotId = serializers.CharField(required=True)
    amount=serializers.IntegerField(required=True)
    currency=serializers.CharField(required=True)
    tokenId=serializers.CharField(required=True)
    description=serializers.CharField(required=False)

class CheckoutResponseSerializer(serializers.Serializer):
    status = serializers.IntegerField()
    message = serializers.ListField()
