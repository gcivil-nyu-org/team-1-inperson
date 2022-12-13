document.onreadystatechange = function () {
    const state = document.readyState
    if (state === 'complete') {
        $('.loading').fadeOut();
    }
}
currentLocation = {};
searchedLocation = {};
var mapLocation =  [-73.98, 40.694];
const mapboxHost = "https://api.mapbox.com/geocoding/v5/mapbox.places/"
const mapboxParams = {"access_token": mapboxgl.accessToken, "types": "address"}
const map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11',
    center: mapLocation,
    zoom: 11
});

filterParams =  Object.fromEntries(new URLSearchParams(document.URL.split('?')[1]));
// Sample lat = 40. long = -74
const infra_types_url = {1:"ramp", 2:"pole", 3:"sidewalk"};
const infra_types = {1:"Accessible Pedestrian Ramps", 2:"Accessible Pedestrian Signals", 3: "Raised Pedestrian Sidewalks"};


if(Object.keys(filterParams).length != 0){
    mapLocation = [ JSON.parse(filterParams['x-co']), JSON.parse(filterParams['y-co'])]
    searchedLocation['longitude'] = JSON.parse(filterParams['x-co']);
    searchedLocation['latitude'] = JSON.parse(filterParams['y-co']);
    plotMap()
}
else {
    getLocation();
}

async function fetchAsync(url) {
  let response = await fetch(url);
  let data = await response.json();
  return data;
}

function highlight_card(infraID) {
    $(".well").removeClass("highlight-card")
    console.log("INFRA ID: ", infraID);
    accessible_locations.forEach(function (accessible_location) {
        if (accessible_location.pk == infraID) {
            fly_to([accessible_location.fields.locationX, accessible_location.fields.locationY], 14)
        }
    });
    const el = document.getElementById(infraID);
    $('#' + infraID).addClass("highlight-card")
    el.scrollIntoView(true);
}

function fly_to(location, zoom_val = 20) {
    map.flyTo({
        center: location,
        essential: true,
        zoom: zoom_val
     });
}

function zoom_map(infraID) {
    console.log("ZOOM_MAP: ", infraID);
    $(".well").removeClass("highlight-card")
    accessible_locations.forEach(function (accessible_location) {

        if (accessible_location.pk == infraID) {
            fly_to([accessible_location.fields.locationX, accessible_location.fields.locationY])
        }
    });
}

function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition, positionError);

  } else {
    console.log("Geolocation is not supported by this device")

  }
}

function showPosition(position) {
    currentLocation['longitude'] = position.coords.longitude;
    currentLocation['latitude'] = position.coords.latitude;
    console.log("currentLocation", currentLocation)
    mapLocation = [position.coords.longitude, position.coords.latitude]
    redirect_to_url();
}

function positionError() {
    alert('Geolocation is not enabled. Please enable to use this feature')
    currentLocation['longitude'] = mapLocation[0];
    currentLocation['latitude'] = mapLocation[1];
    redirect_to_url();
}

function plotMap(){
    map.on('load', function () {
        map.flyTo({
           center: mapLocation,
           essential: true,
           zoom: 14
        });
    });

    const mapboxURL = mapboxHost + mapLocation[0] + "," + mapLocation[1] + ".json?" + new URLSearchParams(mapboxParams)

    fetchAsync(url=mapboxURL).then(response=>{

        const el1 = document.createElement('div1');
        el1.style.backgroundImage = `url('/static/img/pins/pin.png')`;
        el1.className = 'marker';
        el1.style.width = `40px`;
        el1.style.height = `40px`;
        el1.style.backgroundSize = '100%';
        let popupMessage = `<br/><strong>${response["features"][0]["place_name"]}<strong>`

        var marker = new mapboxgl.Marker(el1)
            .setLngLat(mapLocation)
            .setPopup(new mapboxgl.Popup().setHTML(popupMessage))
            .addTo(map);
    });

    map.addControl(
        new mapboxgl.GeolocateControl({
            positionOptions: {
            enableHighAccuracy: true
            },
            trackUserLocation: true,
            showUserHeading: true
        })
    );

    accessible_locations.forEach(function (accessible_location) {

        const isAccessible = accessible_location.fields.isAccessible
        const infraID = accessible_location.pk
        const locX = accessible_location.fields.locationX
        const locY = accessible_location.fields.locationY
        const infraType = accessible_location.fields.typeID
        const isAccessibleString = isAccessible ? "": "Not"
        const pin_url = `/static/img/pins/${infra_types_url[infraType]}-${isAccessible?'a':'na'}.png`

        const el = document.createElement('div');
        el.className = 'marker';
        el.style.backgroundImage = `url(${pin_url})`;
        el.style.width = `40px`;
        el.style.height = `40px`;
        el.style.backgroundSize = '100%';

        const popupMessage = `<br/><strong> ${infra_types[infraType]} </strong>
                              <p>This is currently <strong> ${isAccessibleString} </strong> Accessible </p>`

        var marker = new mapboxgl.Marker(el)
            .setLngLat([locX, locY])
            .setPopup(new mapboxgl.Popup().setHTML(popupMessage))
            .addTo(map);

        marker.getElement().addEventListener('click', (event) =>{
            highlight_card(infraID);
        });
    });

    const geocoder = new MapboxGeocoder({
        accessToken: mapboxgl.accessToken,
        mapboxgl: mapboxgl,
        flyTo: false,
        marker: false,
        bbox: [-74.103684, 40.527645, -73.619187, 40.940556],
        countries: 'US',
    });

    geocoder.on('result', (e) => {
        searchedLocation['longitude'] = e.result.geometry.coordinates[0];
        searchedLocation['latitude'] = e.result.geometry.coordinates[1];
        console.log("searchedLocation", searchedLocation)
        redirect_to_url();
    });

    document.getElementById('geocoder').appendChild(geocoder.onAdd(map));
    map.addControl(new mapboxgl.FullscreenControl());
    map.addControl(new mapboxgl.NavigationControl());
}

function shareLink(){
    var sharePageUrl = document.URL
    navigator.clipboard.writeText(sharePageUrl);
    var shareTooltip = document.getElementById("shareTooltip");
    shareTooltip.innerHTML = "Copied shareable link";
}

function mouseOutShareTooltip() {
  var shareTooltip = document.getElementById("shareTooltip");
  shareTooltip.innerHTML = "Share Address";
}

function copyAddress(text, id){
    navigator.clipboard.writeText(text);
    var copyTooltip = document.getElementById(id);
    copyTooltip.innerHTML = "Copied";
}

function mouseOutCopyTooltip(id) {
  var copyTooltip = document.getElementById(id);
  copyTooltip.innerHTML = "Copy Address";
}