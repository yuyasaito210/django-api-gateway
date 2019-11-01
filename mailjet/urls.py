from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^send_email', views.SendEmail.as_view()),
    url(r'^send_sms', views.SendSms.as_view())
]
