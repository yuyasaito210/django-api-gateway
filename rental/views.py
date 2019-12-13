import json
import requests
import time
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from fcm_django.models import FCMDevice
from drf_yasg.utils import swagger_auto_schema
from .rental_serializers import GetRentalServerResponseSerializer, GetCabinetInfoRequestionSerializer, GetCabinetInfoResponseSerializer, GetAllCabinetInfoResponseSerializer, LendCabinetRequestSerializer, LendCabinetResponseSerializer, LendCabinetCallbackRequestSerializer, LendCabinetCallbackResponseSerializer
from .push_notification_serializers import SendPushNotificationRequestionSerializer, SendPushNotificationResponseSerializer, SendFcmRequestionSerializer, SendFcmResponseSerializer
from mailjet_rest import Client
from .models import RentalServerSetting, RentalRequest
from fcm_django.models import FCMDevice

class GetRentalServer(APIView):
  @swagger_auto_schema(
    request_body=None,
    responses={200: GetRentalServerResponseSerializer(many=False)}
  )
  def get(self, request, format=None):
    '''
    Get rental server info
    '''
    setting = RentalServerSetting.objects.all().first()
    if setting is None:
      raise Response(
        data={'error': 'API gateway don\'t have any rental service settings, yet. Please contact administrator.'},
        status=503
      )

    data = {
      'url': setting.url,
      'name': setting.name,
      'user_name': setting.user_name,
      'password': setting.password,
      'sign': setting.sign
    }
    response_data = {
      'status': 200,
      'message': data
    }
    return Response(data=response_data, status=200)


class GetCabinetInfo(APIView):
  @swagger_auto_schema(
    request_body=GetCabinetInfoRequestionSerializer,
    responses={200: GetCabinetInfoResponseSerializer(many=False)}
  )
  def post(self, request, format=None):
    '''
    Get details info of a cabinet
    '''
    setting = RentalServerSetting.objects.all().first()
    if setting is None:
      raise Response(
        data={'error': 'API gateway don\'t have any rental service settings, yet. Please contact administrator.'},
        status=503
      )

    url = '{base_url}/api/srv/cabinfo'.format(base_url=setting.url)
    body = {
      'sign': setting.sign,
      'body': {
        'stationSn': [request.data['stationSn']]
      }
    }
    headers = {
      'Content-type': 'application/json'
    }

    result = requests.post(url, headers=headers, json=body)
    response_data = result.json()
    response_code = int(response_data['code'])
    if response_code == 200:
      return Response(data=response_data, status=200)
    else:
      return Response(data=None, status=response_code)


class GetAllCabinetInfo(APIView):
  @swagger_auto_schema(
    request_body=None,
    responses={200: GetAllCabinetInfoResponseSerializer(many=False)}
  )
  def post(self, request, format=None):
    '''
    Get stationSn list of all cabinets
    '''
    setting = RentalServerSetting.objects.all().first()
    if setting is None:
      raise Response(
        data={'error': 'API gateway don\'t have any rental service settings, yet. Please contact administrator.'},
        status=503
      )

    url = '{base_url}/api/srv/cablist'.format(base_url=setting.url)
    body = {
      'sign': setting.sign,
      'body': {
        'condition': 'short', # or explicit
        'keyword':'*'
      }
    }
    headers = {
      'Content-type': 'application/json'
    }
    print('==== sending request...')
    result = requests.post(url, headers=headers, json=body)
    print('==== response from middleware: ', result)
    response_data = result.json()
    print('==== response json: ', response_data)
    # response_code = int(response_data['code'])
    
    # if not response_code == 200:
    #   return Response(data=None, status=response_code)
    
    station_sn_list = {
      'stationSnList': response_data['body']
    }

    return Response(data=station_sn_list, status=200)


class LendCabinet(APIView):
  @swagger_auto_schema(
    request_body=LendCabinetRequestSerializer,
    responses={200: LendCabinetResponseSerializer(many=False)}
  )
  def post(self, request, format=None):
    '''
    Lend cabinet
    '''
    setting = RentalServerSetting.objects.all().first()
    if setting is None:
      raise Response(
          data={'error': 'API gateway don\'t have any rental service settings, yet. Please contact administrator.'},
          status=503
        )
    station_sn = request.data['stationSn']
    user_uuid = request.data['uuid']
    push_token = request.data['pushToken']
    device_type = request.data['deviceType']
    trade_no = 'nono-{timeseconds}'.format(timeseconds=int(round(time.time() * 1000))) # Generate tradeNo uuid.
    
    url = '{base_url}/api/srv/lend'.format(base_url=setting.url)
    lend_callback_url = '{callback_base_url}/rental/lend_callback'.format(
      callback_base_url=setting.callback_base_url
    )
    print('==== trade_no: ', trade_no)
    # Send rental request.
    body = {
      'sign': setting.sign,
      'body': {
          'stationSn': station_sn,
          'tradeNo': trade_no,
          'url': lend_callback_url,
          'timeout': 60
        }
    }
    headers = {
      'Content-type': 'application/json'
    }
    print('==== url: ', url)
    try:
      result = requests.post(url, headers=headers, json=body)
    except requests.RequestException as e:
      print('==== error: ', e.message)
      raise Response(
          data={'error': 'API gateway cann\'t send rental request to middleware server. Please try later.'},
          status=403
        )
    
    # print('===== result: ', result['data'])
    response_data = result.json()
    response_code = int(response_data['code'])
    if response_code == 200:
      # Send GCM notification
      fcmDevice = FCMDevice.objects.create(
        registration_id=push_token,
        active=True,
        type=device_type
      )
      # Save current rental request to process callback from station.
      rentalRequest = RentalRequest.objects.create(
        station_sn = station_sn,
        user_uuid = user_uuid,
        device_type = device_type,
        trade_no = trade_no,
        fcm_device_id = fcmDevice.id
      )
      response_data['requestId'] = rentalRequest.id
      
    return Response(data=response_data, status=response_code)


class LendCabinetCallback(APIView):
  @swagger_auto_schema(
    request_body=LendCabinetCallbackRequestSerializer,
    responses={200: LendCabinetCallbackResponseSerializer(many=False)}
  )
  def post(self, request, format=None):
    '''
    Callback API of lend cabinet
    '''
    print('==== lend callback: request_data: ', request.data)
    response_code = int(request.data['code'])
    if response_code == 200:
      # Get data from request
      body = request.data['body']
      trade_no = body['tradeNo']
      power_bank_sn = body['powerBankSn'],
      slot_num = body['slotNum'],
      msg = body['msg']
      # Get rentalRequest and fcmDevice from tradeNo value
      rentalRequest = RentalRequest.objects.filter(trade_no=trade_no).first()
      if rentalRequest:
        fcm_device = rentalRequest.fcm_device
        # Implement FCM
        fcm_data = {
          'type': 'lend_result',
          'data': {
            'tradeNo': trade_no,
            'powerBankSn': power_bank_sn,
            'slotNum': slot_num,
            'msg': msg
          }
        }
        res = fcm_device.send_message(data=fcm_data)
        print('====== res_message: ', res)
        # fcm_device.delete()
        rentalRequest.power_bank_sn = power_bank_sn
        rentalRequest.slot_num = slot_num
        rentalRequest.save()
      else:
        print('====== failed to process callback. don\'t exist rental request for the tradeNo ({trade_no}) '.format(trade_no=trade_no))

    # Return 200 to rental service
    response_data = {
      'msg': '0',
      'code': '200'
    }
    return Response(data=response_data, status=response_code)

class SendPushNotificatioin(APIView):
  @swagger_auto_schema(
    request_body=SendPushNotificationRequestionSerializer,
    responses={200: SendPushNotificationResponseSerializer(many=False)}
  )
  def post(self, request, format=None):
    '''
    Send push notification to device
    '''
    print('==== push notification: request_data: ', request.data)
    registrationId = request.data['registrationId']
    deviceId = request.data['deviceId']
    notification = request.data['notification']
    # Send GCM notification
    device = FCMDevice.objects.create(
      registration_id=registrationId, 
      # device_id=deviceId,
      active=True,
      type='ios'
    )
    res = device.send_message(
      title=notification['title'],
      body=notification['body'],
      data=notification['data']
    )
    print('====== res_notification: ', res)
    device.delete()
    # Return 200 to rental service
    return Response(data=res, status=200)

class SendFcm(APIView):
  @swagger_auto_schema(
    request_body=SendFcmRequestionSerializer,
    responses={200: SendFcmResponseSerializer(many=False)}
  )
  def post(self, request, format=None):
    '''
    Send a FCM (firebase cloud message) to device
    '''
    print('==== push notification: request_data: ', request.data)
    registrationId = request.data['registrationId']
    data_message = request.data['data']
    # Send GCM notification
    device = FCMDevice.objects.create(
      registration_id=registrationId, 
      active=True,
      type='ios'
    )
    res = device.send_message(data=data_message)
    print('====== res_message: ', res)
    device.delete()
    # Return 200 to rental service
    return Response(data=res, status=200)