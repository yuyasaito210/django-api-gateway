from rest_framework import serializers
from drf_yasg.utils import swagger_serializer_method

class SendPushNotificationDataSerializer(serializers.Serializer):
  title = serializers.CharField(required=True)
  body = serializers.CharField(required=True)
  data = serializers.JSONField()

class SendPushNotificationRequestionSerializer(serializers.Serializer):
    registrationId = serializers.CharField(required=True)
    deviceId = serializers.CharField()
    onesignal_user_id = serializers.CharField(required=True)
    notification = SendPushNotificationDataSerializer()

class SendPushNotificationResponseSerializer(serializers.Serializer):
    res = serializers.CharField(required=True)

class SendFcmRequestionSerializer(serializers.Serializer):
    registrationId = serializers.CharField(required=True)
    deviceId = serializers.CharField()
    data = serializers.JSONField(required=True)

class SendFcmResponseSerializer(serializers.Serializer):
    res = serializers.CharField(required=True)
