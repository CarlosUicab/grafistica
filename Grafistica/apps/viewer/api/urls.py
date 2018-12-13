from django.conf.urls import url
from .views import ExcelDataList

app_name = "api"

urlpatterns = [
    url(r'^v1/json/data/$', ExcelDataList.as_view(), name="excel-data"),
]
