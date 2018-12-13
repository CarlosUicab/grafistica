from django.contrib import admin
from .models import ExcelData, DataAnalytic, GraphExcelData, Chart


@admin.register(ExcelData)
class ExcelDataAdmin(admin.ModelAdmin):
    pass


admin.site.register(DataAnalytic)
admin.site.register(Chart)
