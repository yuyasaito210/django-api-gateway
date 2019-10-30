from django.urls import path
from sendmail import views

urlpatterns = [
    path("send_email", views.send_mail),
    path("send_sms", views.send_sms)
]
