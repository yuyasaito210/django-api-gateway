from django.shortcuts import render
from django.http import HttpResponse
from mailjet_rest import Client
from .models import RentalServerSetting
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from .rental_serializers import GetRentalServerResponseSerializer
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
        # Filter talents according to search condition
        body = request.data
        setting = RentalServerSetting.objects.all().first()
        if setting is None:
          raise Response(
            data={
              'error': 'API gateway don\'t have any rental service settings, yet. Please contact administrator.'
            },
            status=503
          )

        'id', 'url', 'name', 'user_name', 'password', 'sign', 'updated_at'

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
        return Response(data=response_data, status=result.status_code)
