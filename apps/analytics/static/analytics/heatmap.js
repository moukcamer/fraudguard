// static/analytics/js/heatmap.js
function initHeatmap(regions) {
    const map = L.map('map').setView([7.0, 12.0], 6);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

    const regionCoords = {
        'Centre (Yaoundé)': [3.8667, 11.5167],
        'Littoral (Douala)': [4.0511, 9.7679],
        'Nord': [9.3, 13.4],
        'Ouest': [5.5, 10.4],
        'Extrême-Nord': [11.0, 14.0],
        'Adamaoua': [7.0, 13.5],
        'Est': [4.0, 14.0],
        'Sud': [2.5, 11.5],
        'Sud-Ouest': [4.2, 9.3],
    };

    regions.forEach(r => {
        const coord = regionCoords[r.region] || [7.0, 12.0];
        const radius = Math.min(r.count * 5, 50);
        L.circle(coord, {
            radius: radius * 1000,
            color: '#e74c3c',
            fillOpacity: 0.5
        }).bindPopup(`${r.region}: ${r.count} cas`).addTo(map);
    });
}