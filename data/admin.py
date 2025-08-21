from django.contrib import admin

from .models import TestResult, CellMeasurement
admin.site.register(TestResult)
admin.site.register(CellMeasurement)
