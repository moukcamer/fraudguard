# apps/reports/serializers.py
from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    evidence = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = Report
        fields = [
            'id', 'description', 'phone_number', 'evidence',
            'risk_score', 'status', 'created_at'
        ]
        read_only_fields = ['risk_score', 'status', 'created_at']

    def create(self, validated_data):
        return Report.objects.create(**validated_data)