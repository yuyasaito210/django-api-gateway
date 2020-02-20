from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from fcm_django.models import FCMDevice

class RentalServerSetting(models.Model):
    name = models.CharField(max_length=50, blank=False, default='')
    url = models.CharField(max_length=100, blank=False, default='')
    user_name = models.CharField(max_length=100, blank=False, default='')
    password = models.CharField(max_length=100, blank=False, default='')
    sign = models.CharField(max_length=100, blank=False, default='')
    callback_base_url = models.CharField(max_length=100, blank=False, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('url', 'updated_at')
        unique_together = ('sign',)
        verbose_name = _("RentalServerSetting")
        verbose_name_plural = _("RentalServerSettings")
        managed = True


class OneSignalSetting(models.Model):
    app_name = models.CharField(max_length=50, blank=False, default='')
    user_auth_key = models.CharField(max_length=256, blank=False, default='')
    app_auth_key = models.CharField(max_length=256, blank=False, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
            return self.app_name

    class Meta:
        ordering = ('app_name', 'updated_at')
        unique_together = ('user_auth_key', 'app_auth_key')
        verbose_name = _("OneSignalSetting")
        verbose_name_plural = _("OneSignalSetting")
        managed = True


class RentalRequest(models.Model):
    station_sn = models.CharField(max_length=32, blank=False, default='')
    user_uuid = models.CharField(max_length=128, blank=False, default='')
    device_type = models.CharField(max_length=10, blank=False, default='ios')
    trade_no = models.CharField(max_length=32, blank=False, default='')
    slot_id = models.IntegerField(blank=True, default=-1)
    power_bank_sn = models.CharField(max_length=32, blank=False, default='')
    fcm_device = models.OneToOneField(
        FCMDevice,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    onesignal_user_id = models.CharField(max_length=255, blank=False, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.trade_no

    class Meta:
        ordering = ('trade_no', 'updated_at')
        unique_together = ('trade_no',)
        verbose_name = _("RentalRequest")
        verbose_name_plural = _("RentalRequest")
        managed = True