from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^server_info', views.GetRentalServer.as_view()),
    url(r'^cabinet_info', views.GetCabinetInfo.as_view()),
    url(r'^cabinet_list', views.GetAllCabinetInfo.as_view()),
    url(r'^lend_cabinet', views.LendCabinet.as_view()),
    url(r'^lend_callback/(?P<pk>[0-9]+)', views.LendCabinetCallback.as_view()),
    url(r'^return_powerbank', views.SettingupReturnNoticeCallback.as_view()),
    # url(r'^return_powerbank', views.ReturnPowerBank.as_view()),
    # url(r'^return_powerbank_callback/(?P<pk>[0-9]+)', views.ReturnPowerBankCallBack.as_view()),
    url(r'^send_push_notification', views.SendPushNotificatioin.as_view()),
    url(r'^send_fcm', views.SendFcm.as_view())
]

views.RegisterReturnPowerBankCallback()