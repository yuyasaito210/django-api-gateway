from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class StripeSetting(models.Model):
    name = models.CharField(max_length=50, blank=False, default='')
    is_live_mode = models.BooleanField(blank=True, default=False)
    live_publishable_key = models.CharField(max_length=100, blank=False, default='')
    live_secret_key = models.CharField(max_length=100, blank=False, default='')
    test_publishable_key = models.CharField(max_length=100, blank=False, default='')
    test_secret_key = models.CharField(max_length=100, blank=False, default='')
    description = models.TextField(max_length=600, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name', 'updated_at')
        unique_together = ('live_publishable_key',)
        verbose_name = _("StripeSetting")
        verbose_name_plural = _("StripeSettings")
        managed = True