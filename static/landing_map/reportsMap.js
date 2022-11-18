function loadReportMap(x, y, card_id){
    new mapboxgl.Marker()
        .setLngLat([x,y])
        .addTo(new mapboxgl.Map({
            container: `map_report_${card_id}`,
            style: 'mapbox://styles/mapbox/streets-v11',
            center: [x,y],
            zoom: 15,
            marker: true
        }));
}