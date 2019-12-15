from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^stripe/checkout', views.StripePayment.as_view()),
    url(r'^stripe/save_card', views.StripeSaveCard.as_view())
]
