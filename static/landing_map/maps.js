const map = new mapboxgl.Map({
    container: 'map',
    // Choose from Mapbox's core styles, or make your own style with Mapbox Studio
    style: 'mapbox://styles/mapbox/streets-v11',
    center: [-74, 40.67],
    zoom: 11
});

const infra_types_url = {1:"ramp", 2:"pole", 3:"sidewalk"};
const infra_types = {1:"Accessible Pedestrian Ramps", 2:"Accessible Pedestrian Signals", 3: "Accessible Pedestrian Sidewalks"};

accessible_locations.forEach(function (accessible_location) {

    const el = document.createElement('div');
    const isAccessible = accessible_location.fields.isAccessible
    const locX = accessible_location.fields.locationX
    const locY = accessible_location.fields.locationY
    const infraType = accessible_location.fields.typeID
    const isAccessibleString = isAccessible ? "": "Not"
    const pin_url = `/static/img/pins/${infra_types_url[infraType]}-${isAccessible?'a':'na'}.png`

    el.className = 'marker';
    el.style.backgroundImage = `url(${pin_url})`;
    el.style.width = `40px`;
    el.style.height = `40px`;
    el.style.backgroundSize = '100%';

    const popupMessage = `<strong> ${infra_types[infraType]} </strong>
                          <p>This is currently <strong> ${isAccessibleString} </strong> Accessible </p>`

    var marker = new mapboxgl.Marker(el)
        .setLngLat([locX, locY])
        .setPopup(new mapboxgl.Popup().setHTML(popupMessage))
        .addTo(map);
});


// Add the control to the map.
const geocoder = new MapboxGeocoder({
    accessToken: mapboxgl.accessToken,
    mapboxgl: mapboxgl,
    zoom: 14
});

geocoder.on('result', (e) => {
    console.log(JSON.stringify(e.result, null, 2))
});

document.getElementById('geocoder').appendChild(geocoder.onAdd(map));
map.addControl(new mapboxgl.FullscreenControl());
map.addControl(new mapboxgl.NavigationControl());