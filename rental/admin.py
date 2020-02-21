from django.contrib import admin
from .models import RentalServerSetting, RentalRequest, OneSignalSetting

@admin.register(RentalServerSetting)
class RentalServerSettingAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'url', 'name', 'user_name', 'password', 'sign', 'updated_at'
    )
    list_display_links = (
        'id', 'url', 'name', 'user_name', 'password', 'sign', 'updated_at'
    )
    list_filter = ('url', 'name', 'sign')
    list_per_page = 25


@admin.register(OneSignalSetting)
class OneSignalSettingAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'app_name', 'app_id', 'app_auth_key', 'user_auth_key', 'updated_at', 'created_at'
    )
    list_display_links = (
        'id', 'app_name', 'app_id', 'app_auth_key', 'user_auth_key', 'updated_at', 'created_at'
    )
    list_filter = ('app_name', 'app_auth_key', 'user_auth_key')
    list_per_page = 25


@admin.register(RentalRequest)
class RentalRequestAdmin(admin.ModelAdmin):
    list_display = (
        'trade_no', 'station_sn', 'slot_id', 'status', 'power_bank_sn',
        'user_uuid', 'device_type',
        'created_at','updated_at'
    )
    list_display_links = (
        'trade_no', 'station_sn', 'slot_id', 'status', 'power_bank_sn',
        'user_uuid', 'device_type',
        'created_at','updated_at'
    )
    list_filter = ('station_sn', 'status', 'user_uuid', 'device_type')
    list_per_page = 50
