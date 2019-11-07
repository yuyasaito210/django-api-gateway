from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^server_info', views.GetRentalServer.as_view())
]
