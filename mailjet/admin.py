from django.contrib import admin
# from rest_framework.authtoken.admin import TokenAdmin
from .models import MailSetting, SmsSetting

@admin.register(MailSetting)
class MailSettingAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'from_email', 'from_name', 'api_key', 'subject', 'text_content', 'updated_at'
    )
    list_display_links = (
        'id', 'from_email', 'from_name', 'api_key', 'subject', 'text_content', 'updated_at'
    )
    list_filter = ('from_email', 'from_name', 'api_key')
    list_per_page = 25


@admin.register(SmsSetting)
class SmsSettingAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'from_title', 'mj_token', 'text_content', 'updated_at'
    )
    list_display_links = (
        'id', 'from_title', 'mj_token', 'text_content', 'updated_at'
    )
    list_filter = ('from_title', 'mj_token', 'text_content')
    list_per_page = 25
