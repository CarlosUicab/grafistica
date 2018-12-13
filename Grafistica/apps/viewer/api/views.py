from rest_framework import generics
from Grafistica.apps.viewer.models import ExcelData
from Grafistica.apps.viewer.api.serializers import ExcelDataSerializer


class ExcelDataList(generics.ListAPIView):
    queryset = ExcelData.objects.all()
    serializer_class = ExcelDataSerializer
    filter_fields = ('excel_name', 'username')

