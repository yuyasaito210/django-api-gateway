from django.shortcuts import render
from django.http import HttpResponse
from mailjet_rest import Client
from .models import MailSetting
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
import json

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")

@api_view(['POST'])
def send_mail(request):
    try:
        setting = MailSetting.objects.all()[:1].get()
    except MailSetting.DoesNotExist:
        setting = MailSetting(
            api_key='e07ff605b7266ba50ca82289887e7690',
            secret_key='d47a84b804a896061aa2c95dd0fba9af',
            from_email='ninjadev999@gmail.com',
            from_name='SMS Sender',
            to_email='br-invin89@hotmail.com',
            to_name='You',
            subject='My first Mailjet Email!',
            text_content='Greetings from Mailjet!',
            html_content='<h3>Dear passenger 1, welcome to <a href=\"https://www.mailjet.com/\">Mailjet</a>!</h3><br />May the delivery force be with you!'
        )
        setting.save()

    api_key = setting.api_key
    secret_key = setting.secret_key
    mailjet = Client(auth=(api_key, secret_key), version='v3.1')
    body = json.loads(request.body)
    to_name = body['to_name']
    to_email = body['to_email']
    data = {
        'Messages': [
            {
                "From": {
                    "Email": setting.from_email,
                    "Name": setting.from_name
                },
                "To": [
                    {
                        "Email": to_email,
                        "Name": to_name
                    }
                ],
                "Subject": setting.subject,
                "TextPart": setting.text_content,
                "HTMLPart": setting.html_content
            }
        ]
    }
    result = mailjet.send.create(data=data)

    return Response(result)

@api_view(['GET', 'POST'])
def send_sms(request):
    url = 'https://api.mailjet.com/v4/sms-send'
    headers = {
        'Authorization': 'Bearer a935f70f75ab4c879718efb96c561c60',
        'Content-type': 'application/json'
    }
    data = {
        'From': 'SMS Sender',
        'To': '+8617624152773',
        'Text': 'Hi!!!'
    }

    result = requests.post(url, headers=headers, json=data)
    return Response(result)
