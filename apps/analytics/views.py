# apps/analytics/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Avg
from apps.reports.models import Report
from apps.accounts.models import User
from django.utils import timezone
from datetime import timedelta


class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Statistiques globales
        total_reports = Report.objects.count()
        fraud_reports = Report.objects.filter(status='fraud').count()
        today_reports = Report.objects.filter(created_at__date=timezone.now().date()).count()

        # Top 5 numéros suspects
        top_numbers = Report.objects.values('phone_number')\
            .annotate(count=Count('id'))\
            .order_by('-count')[:5]

        # Évolution sur 7 jours
        last_7_days = []
        for i in range(6, -1, -1):
            date = timezone.now().date() - timedelta(days=i)
            count = Report.objects.filter(created_at__date=date).count()
            last_7_days.append({"date": date.strftime("%d/%m"), "count": count})

        data = {
            "total_reports": total_reports,
            "fraud_detected": fraud_reports,
            "today_reports": today_reports,
            "fraud_rate": round((fraud_reports / total_reports * 100), 1) if total_reports else 0,
            "top_fraud_numbers": list(top_numbers),
            "last_7_days": last_7_days,
            "active_users": User.objects.filter(is_active=True).count(),
        }

        return Response(data)