from django.shortcuts import render
from django.http import HttpResponse
from mailjet_rest import Client
from .models import RentalServerSetting
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from .rental_serializers import GetRentalServerResponseSerializer, GetCabinetInfoRequestionSerializer, GetCabinetInfoResponseSerializer, GetAllCabinetInfoResponseSerializer, LendCabinetRequestSerializer, LendCabinetResponseSerializer, LendCabinetCallbackRequestSerializer, LendCabinetCallbackResponseSerializer
import requests
import json


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
    #################################################################
    # Wating for new version of rental server.
    # url = '{base_url}/api/srv/cablist'.format(base_url=setting.url)
    # body = {
    #   'sign': setting.sign
    # }
    # headers = {
    #   'Content-type': 'application/json'
    # }

    # result = requests.post(url, headers=headers, json=body)
    # response_data = result.json()
    # response_code = int(response_data['code'])
    # if not response_code == 200:
    #   return Response(data=None, status=response_code)
    
    # station_sn_list = {
    #   'stationSnList': []
    # }
    # for statistation_snonSn in response_data:
    #   station_sn_list['stationSnList'].append(station_sn)

    # return Response(data=station_sn_list, status=200)
    #################################################################

    # For test During wait new version
    station_sn_list = {
      'stationSnList': ['T1219071904']
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

    url = '{base_url}/api/srv/lend'.format(base_url=setting.url)
    lend_callback_url = '{callback_base_url}/rental/lend_cabinet_callback'.format(callback_base_url=setting.callback_base_url)
    print ('=== request.data: ', request.data)
    body = {
    'sign': setting.sign,
    'body': {
        'stationSn': request.data['stationSn'],
        'tradeNo': request.data['tradeNo'],
        'slotNum': request.data['slotNum'],
        'url': lend_callback_url,
        'timeout': 60
      }
    }
    headers = {
      'Content-type': 'application/json'
    }

    result = requests.post(url, headers=headers, json=body)
    response_data = result.json()
    response_code = int(response_data['code'])
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
    print('==== lend callback: ', request.data)
    response_code = 405
    if code in request.data:
       code = int(request.data['code'])
    
    if response_code == 200:
      # Implement Push notification
      push_notification_data = {
        'type': 'lend_result',
        'data': {
          'tradeNo': request.data['body']['tradeNo'],
          'powerBankSn': request.data['body']['powerBankSn'],
          'slotNum': request.data['body']['slotNum'],
          'msg': request.data['body']['msg']
        }
      }
      # Send notificationd data to Firebase
      # send_push_notification(push_notification_data)
    
    # Return 200 to rental service
    response_data = {
      'msg': '0',
      'code': '200'
    }
    return Response(data=response_data, status=response_code)