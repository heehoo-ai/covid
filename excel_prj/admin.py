from django.contrib import admin

# Register your models here.
from excel_prj.models import Sensor


class SensorAdmin(admin.ModelAdmin):
    list_display = ('name', 'isShow')
admin.site.register(Sensor, SensorAdmin)
