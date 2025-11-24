// static/analytics/js/chart.js
fetch('/api/analytics/api/stats/')
    .then(r => r.json())
    .then(data => {
        document.getElementById('total-alerts').textContent = data.total_alerts;
        document.getElementById('total-reports').textContent = data.total_reports;

        // Line Chart: Daily Trend
        new Chart(document.getElementById('trendChart'), {
            type: 'line',
            data: {
                labels: data.daily_trend.map(d => d.day),
                datasets: [{
                    label: 'Alertes',
                    data: data.daily_trend.map(d => d.count),
                    borderColor: '#e74c3c',
                    fill: false
                }]
            },
            options: { responsive: true }
        });

        // Pie Chart: Risk Levels
        new Chart(document.getElementById('riskPie'), {
            type: 'doughnut',
            data: {
                labels: data.risk_breakdown.map(r => r.risk_level),
                datasets: [{
                    data: data.risk_breakdown.map(r => r.count),
                    backgroundColor: ['#27ae60', '#f39c12', '#e67e22', '#c0392b']
                }]
            }
        });

        // Heatmap
        initHeatmap(data.top_regions);
    });