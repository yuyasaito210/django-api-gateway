from django.shortcuts import render
from django.http import HttpResponse
from mailjet_rest import Client
from .models import MailSetting, SmsSetting
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from .email_serializers import SendEmailSerializer, SendEmailResponseSerializer
from .sms_serializers import SendSmsSerializer, SendSmsResponseSerializer
from .phone_verification import generate_verification_code
import requests
import json

class SendEmail(APIView):
    @swagger_auto_schema(
      request_body=SendEmailSerializer,
      responses={200: SendEmailResponseSerializer(many=False)}
    )
    def post(self, request, format=None):
        '''
        Send email
        '''
        # Filter talents according to search condition
        body = request.data
        setting = MailSetting.objects.all().first()
        if setting is None:
          raise Response(
            data={
              'error': 'API gateway don\'t have any mail settings, yet. Please contact administrator.'
            },
            status=503
          )

        api_key = setting.api_key
        secret_key = setting.secret_key
        mailjet = Client(auth=(api_key, secret_key), version='v3.1')
        body = request.data
        to_name = body['to_name']
        to_email = body['to_email']
        data = {
            'Messages': [
                {
                    'From': {
                        'Email': setting.from_email,
                        'Name': setting.from_name
                    },
                    'To': [
                        {
                            'Email': to_email,
                            'Name': to_name
                        }
                    ],
                    'Subject': setting.subject,
                    'TextPart': setting.text_content,
                    'HTMLPart': setting.html_content
                }
            ]
        }
        result = mailjet.send.create(data=data)
        response_data = {
          'status': result.status_code,
          'message': result.json()
        }
        return Response(data=response_data, status=result.status_code)


class SendSms(APIView):
    @swagger_auto_schema(
        request_body=SendSmsSerializer,
        responses={200: SendSmsResponseSerializer(many=False)}
    )
    def post(self, request, format=None):
        setting = SmsSetting.objects.all().first()
        if setting is None:
            raise Response(
                data={
                  'error': 'API gateway don\'t have any sms settings, yet. Please contact administrator.'
                },
                status=503
            )
        # Generate verification code
        verification_code = generate_verification_code()

        url = 'https://api.mailjet.com/v4/sms-send'

        body = request.data
        headers = {
            'Authorization': 'Bearer {sms_token}'.format(sms_token=setting.mj_token),
            'Content-type': 'application/json'
        }
        data = {
            'From': setting.from_title,
            'To': body['to_telnumber'],
            'Text': verification_code
        }

        result = requests.post(url, headers=headers, json=data)

        response_data = {
          'status': result.status_code,
          'message': {
            'verification_code': verification_code,
            'res': result.json()
          }
        }
        return Response(data=response_data, status=result.status_code)
