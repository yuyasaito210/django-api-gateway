from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


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