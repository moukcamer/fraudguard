// static/js/main.js
document.addEventListener("DOMContentLoaded", () => {
    console.log("FraudGuard loaded - Cameroon Time:", new Date().toLocaleString("fr-CM"));

    // Auto-refresh risk score every 30s (if on dashboard)
    if (window.location.pathname.includes("dashboard")) {
        setInterval(() => {
            fetch("/api/v1/fraud/risk/")
                .then(r => r.json())
                .then(data => {
                    document.getElementById("live-risk").textContent = data.risk_score.toFixed(2);
                });
        }, 30000);
    }
});