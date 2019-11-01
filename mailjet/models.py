from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class MailSetting(models.Model):
    name = models.CharField(max_length=50, blank=False, default='')
    api_key = models.CharField(max_length=100, blank=False, default='')
    secret_key = models.CharField(max_length=100, blank=False, default='')
    from_email = models.CharField(max_length=200, blank=False, default='')
    from_name = models.CharField(max_length=200, blank=False, default='')
    subject = models.CharField(max_length=200, blank=True, default='')
    text_content = models.TextField(blank=True, default='')
    html_content = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('from_email', 'updated_at')
        unique_together = ('api_key',)
        verbose_name = _("MailSetting")
        verbose_name_plural = _("MailSettings")
        managed = True


class SmsSetting(models.Model):
    name = models.CharField(max_length=50, blank=False, default='')
    mj_token = models.CharField(max_length=100, blank=False, default='')
    from_title = models.CharField(max_length=100, blank=False, default='')
    text_content = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('from_title', 'updated_at')
        unique_together = ('mj_token',)
        verbose_name = _("SmsSetting")
        verbose_name_plural = _("SmsSettings")
        managed = True