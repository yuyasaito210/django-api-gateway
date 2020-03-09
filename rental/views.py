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
import onesignal as onesignal_sdk
from .rental_serializers import GetRentalServerResponseSerializer, GetCabinetInfoRequestionSerializer, GetCabinetInfoResponseSerializer, GetAllCabinetInfoResponseSerializer, LendCabinetRequestSerializer, LendCabinetResponseSerializer, LendCabinetCallbackRequestSerializer, LendCabinetCallbackResponseSerializer, ReturnPowerBankRequestSerializer, ReturnPowerBankResponseSerializer, ReturnPowerBankCallbackRequestSerializer, ReturnPowerBankCallbackResponseSerializer, SettingupReturnNoticeCallbackRequestSerializer, SettingupReturnNoticeCallbackResponseSerializer
from .push_notification_serializers import SendPushNotificationRequestionSerializer, SendPushNotificationResponseSerializer, SendFcmRequestionSerializer, SendFcmResponseSerializer
from mailjet_rest import Client
from .models import RentalServerSetting, RentalRequest, OneSignalSetting
from fcm_django.models import FCMDevice


def create_notification_client():
  onsignalSetting = OneSignalSetting.objects.all().first()
  if onsignalSetting:
    return onesignal_sdk.Client(
      app_auth_key=onsignalSetting.app_auth_key,
      app_id=onsignalSetting.app_id
    )

def send_onesignal_notification(headings, contents, data_type, data, ids):
  onesignal_client = create_notification_client()
  if onesignal_client:
    new_notification = onesignal_sdk.Notification(
      post_body={
        'headings': {'en': headings},
        'contents': {
          'en': contents
        },
        'data': {
          'type': data_type,
          'data': data
        },
        'include_player_ids': ids,
      }
    )
    onesignal_response = onesignal_client.send_notification(new_notification)


def RegisterReturnPowerBankCallback():
  print('==== Setting up Return Notice.')
  setting = RentalServerSetting.objects.all().first()
  if setting is None:
    print('===== Failed to Setting up Return Notice: did not get rental server setting.')

  # Send rental request.
  url = '{base_url}/api/srv/setupBaction'.format(base_url=setting.url)
  return_powerbank_callback_url = '{callback_base_url}/rental/return_powerbank'.format(
    callback_base_url=setting.callback_base_url
  )
  body = {
    'sign': setting.sign,
    'body': {
        'url': return_powerbank_callback_url
      }
  }
  headers = {
    'Content-type': 'application/json'
  }
  print('==== url: ', url)
  print('==== body: ', body)
  try:
    result = requests.post(url, headers=headers, json=body)
    response_data = result.json()
    print('===== Success to Setting up Return Notice. ', response_data)

  except:
    print('===== Failed to Setting up Return Notice.')
    

def SendCallbackResponse():
  # Get sign info
  setting = RentalServerSetting.objects.all().first()
  sign_cache = setting.sign[-5:]
  # send failed notification
  response_data = sign_cache
  print("==== send response with sign_cache {sign_cache} to callback request.".format(sign_cache=sign_cache))
  return Response(data=response_data, headers={'Content-type': 'text/plain;charset=UTF-8'}, status=200)

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
          data={
            'error': 'API gateway don\'t have any rental service settings, yet. Please contact administrator.'
          },
          status=503
        )
    print('==== request.data: ', request.data)
    station_sn = request.data['stationSn']
    user_uuid = request.data['uuid']
    push_token = request.data['pushToken']
    device_type = request.data['deviceType']
    onesignal_user_id = request.data['onesignalUserId']

    rental_request = RentalRequest.objects.create(
      station_sn = station_sn,
      user_uuid = user_uuid,
      device_type = device_type,
      # trade_no = trade_no,
      slot_id = 0,
      onesignal_user_id = onesignal_user_id,
      status = RentalRequest.REQUIRED_RENT
    )
    print('===== rental_request.id: ', rental_request.id)
    trade_no = '{tradeNo}'.format(tradeNo=rental_request.id)
    rental_request.trade_no = trade_no
    rental_request.save()

    url = '{base_url}/api/srv/lend'.format(base_url=setting.url)
    lend_callback_url = '{callback_base_url}/rental/lend_callback/{request_id}'.format(
      callback_base_url=setting.callback_base_url,
      request_id=rental_request.id
    )
    # Send rental request.
    body = {
      'sign': setting.sign,
      'body': {
          'stationSn': station_sn,
          'tradeNo': trade_no,
          'slotNum': 0,
          'url': lend_callback_url,
          'timeout': 60
        }
    }
    headers = {
      'Content-type': 'application/json'
    }
    print('==== url: ', url)
    print('==== body: ', body)
    try:
      result = requests.post(url, headers=headers, json=body)
      response_data = result.json()
      print('===== response_data: ', response_data)
      response_code = int(response_data['code'])
      msg = int(response_data['msg'])
      print('===== response_code: ', response_code)
      if (response_code == 200) and (msg == 0):
        response_data['tradeNo'] = trade_no
      
        return Response(data=response_data, status=response_code)
      else:
        return Response(
          data={'error': 'Middleware server have some problem now. Please try later.'},
          status=403
        )

    except:
      return Response(
        data={'error': 'API gateway cann\'t send rental request to middleware server. Please try later.'},
        status=403
      )


class LendCabinetCallback(APIView):

  @swagger_auto_schema(
    request_body=LendCabinetCallbackRequestSerializer,
    responses={200: LendCabinetCallbackResponseSerializer(many=False)}
  )
  def post(self, request, pk, format=None):
    '''
    Callback API of lend cabinet
    '''
    print('==== lend callback: request_data: ', request.data)

    # Get sign info
    setting = RentalServerSetting.objects.all().first()
    sign_cache = setting.sign[-5:]

    rental_request = RentalRequest.objects.filter(id=pk).first()
    response_code = int(request.data['code'])

    if rental_request is None:
      print('====== failed to process callback. don\'t exist rental request for the tradeNo ({trade_no}) '.format(trade_no=pk))
      # send failed notification
      response_data = sign_cache
      print("==== send response with sign_cache {sign_cache} to callback request.".format(sign_cache=sign_cache))
      return Response(data=response_data, headers={'Content-type': 'text/plain;charset=UTF-8'}, status=200)

    if rental_request.status != RentalRequest.REQUIRED_RENT:
      print('===== skip the duplicated rent-buttery callbacks')
      response_data = sign_cache
      print("==== send response with sign_cache {sign_cache} to callback request.".format(sign_cache=sign_cache))
      return Response(data=response_data, headers={'Content-type': 'text/plain;charset=UTF-8'}, status=200)

    status = RentalRequest.RENTED
    if response_code == 200:
      # Get data from request
      body = request.data['body']
      trade_no = body['tradeNo']
      power_bank_sn = body['powerBankSn']
      slot_num = int(body['slotNum'])
      msg = int(body['msg'])
      
      # Make notification data
      data = {
        'stationSn': rental_request.station_sn,
        'tradeNo': trade_no,
        'powerBankSn': power_bank_sn,
        'slotNum': slot_num,
        'msg': msg
      }
      ids = [rental_request.onesignal_user_id]

      print('==== msg: ', msg)
      if msg == 0:          
        headings = 'Rent Buttery'
        data_type = 'RENT_BATTERY'
        contents = 'You rented {station_sn} succesfully. PowerBank: {power_bank_sn}, SlotNumber: {slot_num}'.format(
          station_sn = rental_request.station_sn, power_bank_sn=power_bank_sn, slot_num=slot_num
        )
        print('==== send: success notification')
        send_onesignal_notification(headings, contents, data_type, data, ids)
        status = RentalRequest.RENTED
      else:
        headings = 'Fialed To Rent Buttery'
        data_type = 'FAILED_RENT_BATTERY'
        contents = 'You are failed to rent a buttery on the station {station_sn}. Please try again'.format(
          station_sn=rental_request.station_sn
        )
        print('==== send: failed notification')
        send_onesignal_notification(headings, contents, data_type, data, ids)
        status = RentalRequest.RENT_FAILED
        
      rental_request.power_bank_sn = power_bank_sn
      rental_request.slot_id = slot_num
        
    else:
      print('====== failed to process callback. don\'t exist rental request for the tradeNo ({trade_no}) '.format(trade_no=pk))
      # send failed notification
      headings = 'Fialed To Rent Buttery'
      data_type = 'FAILED_RENT_BATTERY'
      contents = 'You are failed to rent a buttery on the station {station_sn}. Please try again'.format(
        station_sn=rental_request.station_sn
      )
      data = {
        'stationSn': rental_request.station_sn,
        'tradeNo': '{pk}'.format(pk=pk),
        'powerBankSn': '0',
        'slotNum': '0',
        'msg': '0'
      }
      ids = [rental_request.onesignal_user_id]
      send_onesignal_notification(headings, contents, data_type, data, ids)
      status = RentalRequest.RENT_FAILED

    rental_request.status = status
    rental_request.save()

    # Return 200 to rental service
    print("==== send response with sign_cache {sign_cache} to callback request.".format(sign_cache=sign_cache))
    response_data = sign_cache
    return Response(data=response_data, headers={'Content-type': 'text/plain;charset=UTF-8'}, status=200)


class ReturnPowerBank(APIView):
  @swagger_auto_schema(
    request_body=ReturnPowerBankRequestSerializer,
    responses={200: ReturnPowerBankResponseSerializer(many=False)}
  )
  def post(self, request, format=None):
    '''
    Lend cabinet
    '''
    setting = RentalServerSetting.objects.all().first()
    if setting is None:
      raise Response(
          data={
            'error': 'API gateway don\'t have any rental service settings, yet. Please contact administrator.'
          },
          status=503
        )
    print('====== ReturnPowerBank: request.data: ', request.data)
    station_sn = request.data['stationSn']
    trade_no = request.data['tradeNo']
    push_token = request.data['pushToken']
    slot_num = request.data['slotNum']
    uuid = request.data['uuid']
    onesignal_user_id = request.data['onesignalUserId']
    
    rental_request = RentalRequest.objects.filter(trade_no=trade_no).first()
    
    url = '{base_url}/api/dev/pbyet'.format(base_url=setting.url)
    return_powerbank_callback_url = '{callback_base_url}/rental/return_powerbank_callback'.format(
      callback_base_url=setting.callback_base_url
    )
    # Send rental request.
    body = {
      'sign': setting.sign,
      'body': {
          'stationSn': station_sn,
          'tradeNo': trade_no,
          'slotNum': slot_num,
          'url': return_powerbank_callback_url
        }
    }
    headers = {
      'Content-type': 'application/json'
    }
    print('==== url: ', url)
    print('==== body: ', body)
    try:
      result = requests.post(url, headers=headers, json=body)
      response_data = result.json()
      print('===== response_data: ', response_data)
      response_code = int(response_data['code'])
      print('===== response_code: ', response_code)
      if response_code == 200:
        response_data['tradeNo'] = trade_no
      
      rental_request.status = RentalRequest.REQUIRED_RETURN
      rental_request.save()
      return Response(data=response_data, status=response_code)

    except:
      return Response(
        data={'error': 'API gateway cann\'t send rental request to middleware server. Please try later.'},
        status=403
      )

class ReturnPowerBankCallBack(APIView):
  @swagger_auto_schema(
    request_body=ReturnPowerBankCallbackRequestSerializer,
    responses={200: ReturnPowerBankCallbackResponseSerializer(many=False)}
  )
  def post(self, request, pk, format=None):
    '''
    Callback API of lend cabinet
    '''
    print('==== return_powerbank callback: request_data: ', request.data)
    rental_request = RentalRequest.objects.filter(id=pk).first()
    response_code = int(request.data['code'])

    if rental_request is None:
      print('====== failed to process the return-buttery callback. don\'t exist rental request for the tradeNo ({trade_no}) '.format(trade_no=pk))
      # send failed notification
      response_data = {'msg': '0', 'code': '403'}
      return Response(data=response_data, status=403)
    
    if rental_request.status == RentalRequest.REQUIRED_RETURN:
      print('====== skip the duplicated return_buttery callback')
      response_data = {'msg': '0', 'code': '200'}
      return Response(data=response_data, status=200)

    status = RentalRequest.RETURNED
    if response_code == 200:
      # Get data from request
      body = request.data['body']
      power_bank_sn = body['powerBankSn']
      slot_num = int(body['slotNum'])
      trade_no = body['tradeNo']
      code = body['code']
      rs_code = body['rsCode']
      station_no = body['stationNo']
      linestatus = body['linestatus']
      lockstatus = body['lockstatus']
      ele = body['ele']
      msg = body['msg']

      # Make notification data
      data = body
      ids = [rental_request.onesignal_user_id]
      print('==== msg: ', msg)
      if msg == 0:
        headings = 'Return Buttery'
        data_type = 'RETURN_BATTERY'
        contents = 'You returned the buttery succesfully. PowerBank: {power_bank_sn}, SlotNumber: {slot_num}'.format(
          power_bank_sn=power_bank_sn, slot_num=slot_num
        )
        print('==== send: success notification')
        send_onesignal_notification(headings, contents, data_type, data, ids)
        status = RentalRequest.RETURNED
      else:
          headings = 'Fialed To Return Buttery'
          data_type = 'FAILED_RETURN_BATTERY'
          contents = 'You are failed to return the buttery on the station {station_sn}. Please try again'.format(
            station_sn=rental_request.station_sn
          )
          print('==== send: failed notification')
          send_onesignal_notification(headings, contents, data_type, data, ids)
          status = RentalRequest.RETURN_FAILED
       
    else:
      # send failed notification
      headings = 'Fialed To Return Buttery'
      data_type = 'FAILED_RETURN_BATTERY'
      contents = 'You are failed to return the buttery on the station {station_sn}. Please try again'.format(
        station_sn=rental_request.station_sn
      )
      data = {
        'stationSn': rental_request.station_sn,
        'tradeNo': '{pk}'.format(pk=pk),
      }
      ids = [rental_request.onesignal_user_id]
      send_onesignal_notification(headings, contents, data_type, data, ids)
      status = RentalRequest.RENT_FAILED

    # Return 200 to rental service
    response_data = {
      'msg': '0',
      'code': '200'
    }
    return Response(data=response_data, status=response_code)


class SettingupReturnNoticeCallback(APIView):
  @swagger_auto_schema(
    request_body=SettingupReturnNoticeCallbackRequestSerializer,
    responses={200: SettingupReturnNoticeCallbackResponseSerializer(many=False)}
  )
  def post(self, request, format=None):
    '''
    Callback API of Setting up Return Notice
    '''
    data = request.data
    print('==== Return Notice callback: request_data: ', data)
    code = data['code']
    rsCode = data['rsCode']
    powerBankSn = data['powerBankSn']
    slotNum = int(data['slotNum'])
    stationNo = data['stationNo']

    rental_request = RentalRequest.objects.filter(
      power_bank_sn=powerBankSn, slot_id=slotNum
    ).first()
    if rental_request is None:
      print('====== Failed to return buttery. The statinSn ({stationNo}) and slotNum({slotNum}) do not exist in request list.'.format(
        stationNo=stationNo, slotNum=slotNum
      ))
      return SendCallbackResponse()

    if (code == 200) and (rsCode == "1"):
      # success and send notification to app
      linestatus = data['linestatus']
      lockstatus = data['lockstatus']
      retTime = data['Retime']
      ele = data['ele']
      msg = data['msg']
      # Check duplcation
      if rental_request.status == RentalRequest.RETURNED:
        print('====== skip the duplicated return_buttery callback')
        return SendCallbackResponse()

      # Make notification data
      ids = [rental_request.onesignal_user_id]
      print('==== msg: ', msg)
      if msg == 0:
        headings = 'Return Buttery'
        data_type = 'RETURNED'
        contents = 'You returned the buttery succesfully. PowerBankSn: {powerBankSn}, SlotNumber: {slotNum}'.format(
          powerBankSn=powerBankSn, slotNum=slotNum
        )
        print('==== send: success notification')
        send_onesignal_notification(headings, contents, data_type, data, ids)
        status = RentalRequest.RETURNED
      else:
        headings = 'Fialed To Return Buttery'
        data_type = 'FAILED_RETURN_BATTERY'
        contents = 'You are failed to return the buttery on the powerBankSn {power_bank_sn}. Please try again'.format(
          power_bank_sn=rental_request.power_bank_sn
        )
        print('==== send: failed notification')
        send_onesignal_notification(headings, contents, data_type, data, ids)
        status = RentalRequest.RETURN_FAILED
    else:
      # send failed notification
      headings = 'Fialed To Return Buttery'
      data_type = 'FAILED_RETURN_BATTERY'
      contents = 'You are failed to return the buttery on the powerBankSn {power_bank_sn}. Please try again'.format(
        power_bank_sn=rental_request.power_bank_sn
      )
      data = {
        'stationSn': rental_request.power_bank_sn,
        'slotNum': rental_request.slot_id,
      }
      ids = [rental_request.onesignal_user_id]
      send_onesignal_notification(headings, contents, data_type, data, ids)
      status = RentalRequest.RENT_FAILED

    rental_request.status = status
    rental_request.save

    return SendCallbackResponse()


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
    # registrationId = request.data['registrationId']
    # deviceId = request.data['deviceId']
    onesignal_user_id = request.data['onesignal_user_id']
    notification = request.data['notification']

    # Send GCM notification
    # device = FCMDevice.objects.create(
    #   registration_id=registrationId, 
    #   # device_id=deviceId,
    #   active=True,
    #   type='ios'
    # )
    # res = device.send_message(
    #   title=notification['title'],
    #   body=notification['body'],
    #   data=notification['data']
    # )
    # print('====== res_notification: ', res)
    # device.delete()

    # Send Onsignal Push notification
    onsignalSetting = OneSignalSetting.objects.all().first()
    if onsignalSetting:
      onesignal_client = onesignal_sdk.Client(
        app_auth_key=onsignalSetting.app_auth_key,
        app_id=onsignalSetting.app_id
      )
      new_notification = onesignal_sdk.Notification(
        post_body={
          'headings': {'en': notification['title']},
          'contents': {'en': notification['body']},
          'data': notification['data'],
          'include_player_ids': [onesignal_user_id,],
        }
      )

      # send notification, it will return a response
      onesignal_response = onesignal_client.send_notification(new_notification)
      print('====== onesignal_response.status_code: ', onesignal_response.status_code)
      print('====== onesignal_response.json: ', onesignal_response.json())
    
    # Return 200 to rental service
    return Response(data=onesignal_response, status=200)


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
