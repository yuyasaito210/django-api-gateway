from django.contrib import admin
from .models import RentalServerSetting

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

