
const map = L.map('map').setView([54, 15], 4);


L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);


async function haeKentat() {

    const response = await fetch('/api/airports');

    const airports = await response.json();


    const locations = [];


    airports.forEach(airport => {

        const marker = L.circleMarker(
            [airport.lat, airport.lon],
            {
                radius: 6,
                color: 'red',
                fillColor: 'red',
                fillOpacity: 0.8
            }
        ).addTo(map);


        marker.bindPopup(`
            <b>${airport.name}</b><br>
            ICAO: ${airport.icao}
        `);

        locations.push([airport.lat, airport.lon]);

    });


    if (locations.length > 0) {
        map.fitBounds(locations, {
            padding: [30, 30]
        });
    }
}


haeKentat();
