from rest_framework import serializers
from drf_yasg.utils import swagger_serializer_method

class GetRentalServerResponseSerializer(serializers.Serializer):
    url = serializers.CharField(required=True)
    user_name = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    sign = serializers.CharField(required=True)
    callback_base_url = serializers.CharField(required=True)

class GetCabinetInfoRequestionSerializer(serializers.Serializer):
    stationSn = serializers.CharField(required=True)

class GetCabinetInfoResponseSerializer(serializers.Serializer):
    lastupline = serializers.CharField(required=True)
    lastActive = serializers.CharField(required=True)
    isOnline = serializers.IntegerField(required=True)
    slotList = serializers.ListField(required=True)
    slotTotal = serializers.IntegerField(required=True)
    areaCode = serializers.CharField(required=True)
    slotStatus = serializers.CharField(required=True)
    versions = serializers.CharField(required=True)
    lastdownline = serializers.CharField(required=True)
    imei = serializers.CharField(required=True)
    topic = serializers.CharField(required=True)
    baseStation = serializers.CharField(required=True)
    stationSn = serializers.CharField(required=True)
    status = serializers.IntegerField(required=True)

class GetAllCabinetInfoResponseSerializer(serializers.Serializer):
    stationSnList = serializers.ListField(child=serializers.CharField(), required=True)

class LendCabinetRequestSerializer(serializers.Serializer):
    stationSn = serializers.CharField(required=True)
    uuid = serializers.CharField(required=True)
    pushToken = serializers.CharField(required=True)
    deviceType = serializers.CharField(required=True)
    onesignalUserId = serializers.CharField(required=True)

class LendCabinetResponseSerializer(serializers.Serializer):
    msg = serializers.CharField(required=True)
    code = serializers.IntegerField(required=True)
    requestId = serializers.IntegerField()

class LendCabinetCallbackRequestSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    body = serializers.JSONField(required=True)
    # tradeNo = serializers.CharField(required=True)
    # powerBankSn = serializers.CharField(required=True)
    # slotNum = serializers.IntegerField(required=True)

class LendCabinetCallbackResponseSerializer(serializers.Serializer):
    msg = serializers.CharField(required=True)
    code = serializers.IntegerField(required=True)


class ReturnPowerBankRequestSerializer(serializers.Serializer):
    stationSn = serializers.CharField(required=True)
    tradeNo = serializers.CharField(required=True)
    slotNum = serializers.CharField(required=True)
    uuid = serializers.CharField(required=True)
    onesignalUserId = serializers.CharField(required=True)

class ReturnPowerBankResponseSerializer(serializers.Serializer):
    msg = serializers.CharField(required=True)
    code = serializers.CharField(required=True)

class ReturnPowerBankCallbackRequestSerializer(serializers.Serializer):
    msg = serializers.IntegerField(required=True)
    powerBankSn = serializers.CharField(required=True)
    slotNum = serializers.CharField(required=True)
    code = serializers.IntegerField(required=True)
    rsCode = serializers.IntegerField(required=True)
    stationNo = serializers.CharField(required=True)
    linestatus = serializers.CharField(required=True)
    lockstatus = serializers.CharField(required=True)
    ele = serializers.CharField(required=True)

class ReturnPowerBankCallbackResponseSerializer(serializers.Serializer):
    msg = serializers.CharField(required=True)
    code = serializers.IntegerField(required=True)