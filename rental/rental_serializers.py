from rest_framework import serializers
from drf_yasg.utils import swagger_serializer_method

class GetRentalServerResponseSerializer(serializers.Serializer):
    url = serializers.CharField(required=True)
    user_name = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    sign = serializers.CharField(required=True)
