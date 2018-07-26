from django.contrib import admin
from gps import models


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('imei', 'last_position_datetime', 'last_position_view_link', )


class PositionAdmin(admin.ModelAdmin):
    list_filter = ('datetime', 'device__imei',)
    list_display = ('device', 'datetime', 'position', 'view_link', )
    readonly_fields = ('device', 'latitude', 'longitude', 'datetime', 'view_link',)

    list_display_links = ('position',)


admin.site.register(models.Device, DeviceAdmin)
admin.site.register(models.Position, PositionAdmin)
