from django.urls import path
from django.conf.urls import include, url
from . import views

urlpatterns = [
    path("send_email", views.SendEmail.as_view()),
    path("send_sms", views.SendSms.as_view())
]
