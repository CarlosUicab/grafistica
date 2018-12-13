from rest_framework import serializers
from Grafistica.apps.viewer.models import ExcelData


class ExcelDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExcelData
        fields = '__all__'



