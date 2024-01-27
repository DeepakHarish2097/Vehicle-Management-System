from django.contrib import admin
from . import models


admin.site.register(models.Employee)
admin.site.register(models.Route)
admin.site.register(models.Vehicle)
admin.site.register(models.Productivity)
