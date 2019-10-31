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
            status=404
          )
          # setting = MailSetting(
          #     api_key='e07ff605b7266ba50ca82289887e7690',
          #     secret_key='d47a84b804a896061aa2c95dd0fba9af',
          #     from_email='ninjadev999@gmail.com',
          #     from_name='SMS Sender',
          #     to_email='br-invin89@hotmail.com',
          #     to_name='You',
          #     subject='My first Mailjet Email!',
          #     text_content='Greetings from Mailjet!',
          #     html_content='<h3>Dear passenger 1, welcome to <a href=\'https://www.mailjet.com/\'>Mailjet</a>!</h3><br />May the delivery force be with you!'
          # )
          # setting.save()

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
        if result.status_code == 200:
          return Response(data=result.json(), status=result.status_code)
        
        return Response({'error': result.json()}, status=result.status_code)

# @api_view(['POST'])
# def send_mail(request):
    

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
                status=404
            )
        
        url = 'https://api.mailjet.com/v4/sms-send'

        body = request.data
        headers = {
            'Authorization': 'Bearer {sms_token}'.format(sms_token=setting.mj_token),
            'Content-type': 'application/json'
        }
        data = {
            'From': setting.from_title,
            'To': body['to_telnumber'],
            'Text': setting.text_content #? must be replaced with verification code
        }

        result = requests.post(url, headers=headers, json=data)

        if result.status_code == 200:
          return Response(data=result.json(), status=result.status_code)
        
        return Response({'error': result.json()}, status=result.status_code)