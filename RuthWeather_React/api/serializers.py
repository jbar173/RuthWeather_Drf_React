from rest_framework import serializers
from . import models


class AmSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Am
        fields = '__all__'

class PmSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Pm
        fields = '__all__'

class EveSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Eve
        fields = '__all__'

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Report
        fields = '__all__'
