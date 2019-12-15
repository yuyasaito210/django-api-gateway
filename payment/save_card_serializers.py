from rest_framework import serializers
from drf_yasg.utils import swagger_serializer_method

class SaveCardSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    tokenId = serializers.CharField(required=True)

class SaveCardResponseSerializer(serializers.Serializer):
    status = serializers.IntegerField()
    message = serializers.ListField()
