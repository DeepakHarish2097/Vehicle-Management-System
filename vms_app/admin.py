from django.contrib import admin
from . import models


admin.site.register(models.Employee)
admin.site.register(models.Route)
admin.site.register(models.Vehicle)
admin.site.register(models.Productivity)
admin.site.register(models.Workshop)
admin.site.register(models.Zone)
admin.site.register(models.Ward)
admin.site.register(models.TransferRegister)
admin.site.register(models.IncidentLog)
