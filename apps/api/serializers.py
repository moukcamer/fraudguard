# apps/api/serializers.py
from rest_framework import serializers
from apps.fraud_detection.models import FraudAlert
from apps.reports.models import FraudReport

class FraudAlertAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = FraudAlert
        fields = ['id', 'risk_score', 'risk_level', 'reason', 'created_at']
        read_only_fields = fields

class FraudReportAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = FraudReport
        fields = ['id', 'report_type', 'target_phone', 'description', 'status', 'created_at']
        read_only_fields = ['status', 'created_at']