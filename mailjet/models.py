from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class MailSetting(models.Model):
    api_key = models.CharField(max_length=100)
    secret_key = models.CharField(max_length=100)
    from_email = models.CharField(max_length=200)
    from_name = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    text_content = models.TextField(blank=True, default='')
    html_content = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{from_email}: {api_key}'.format(
            from_email=self.from_email,
            api_key=self.api_key
        )

    class Meta:
        ordering = ('from_email', 'updated_at')
        unique_together = ('api_key',)
        verbose_name = _("MailSetting")
        verbose_name_plural = _("MailSettings")
        managed = True


class SmsSetting(models.Model):
    mj_token = models.CharField(max_length=100)
    from_title = models.CharField(max_length=100)
    text_content = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{from_title}: {mj_token}'.format(
            from_title=self.from_title,
            mj_token=self.mj_token
        )

    class Meta:
        ordering = ('from_title', 'updated_at')
        unique_together = ('mj_token',)
        verbose_name = _("SmsSetting")
        verbose_name_plural = _("SmsSettings")
        managed = True