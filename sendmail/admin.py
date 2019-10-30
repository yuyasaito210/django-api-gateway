from django.contrib import admin
from .models import MailSetting

class MailSettingAdmin(admin.ModelAdmin):
    list_display=('api_key', 'secret_key')

admin.site.register(MailSetting, MailSettingAdmin)
