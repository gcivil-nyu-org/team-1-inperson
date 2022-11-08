currentLocation = {};
searchedLocation = {};
var mapLocation =  [-73.98, 40.694];
//const mapboxHost = "https://api.mapbox.com/geocoding/v5/mapbox.places/"
//const mapboxParams = {"access_token": mapboxgl.accessToken, "types": "address"}

filterParams =  Object.fromEntries(new URLSearchParams(document.URL.split('?')[1]));
// Sample lat = 40. long = -74
const infra_types_url = {1:"ramp", 2:"pole", 3:"sidewalk"};
const infra_types = {1:"Accessible Pedestrian Ramps", 2:"Accessible Pedestrian Signals", 3: "Raised Pedestrian Sidewalks"};


if(Object.keys(filterParams).length != 0){
    mapLocation = [ JSON.parse(filterParams['x-co']), JSON.parse(filterParams['y-co'])]
    searchedLocation['longitude'] = JSON.parse(filterParams['x-co']);
    searchedLocation['latitude'] = JSON.parse(filterParams['y-co']);
    //plotMap()
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
    $(".well").css("color", "black");
    console.log("INFRA ID: ", infraID);
    const el = document.getElementById(infraID);
    $('#' + infraID).css("color", "red");
    el.scrollIntoView(true);
}

function zoom_map(infraID) {
    console.log("ZOOM_MAP: ", infraID);
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


//geocoder

const geocoder = new MapboxGeocoder({
accessToken: mapboxgl.accessToken,
proximity: {
    longitude: -73.98,
    latitude: 40.694
  }
});


geocoder.addTo('#geocoder-low-vision');

// Get the geocoder results container.
// const results = document.getElementById('result');

geocoder.on('result', (e) => {
    searchedLocation['longitude'] = e.result.geometry.coordinates[0];
    searchedLocation['latitude'] = e.result.geometry.coordinates[1];
    console.log("searchedLocation", searchedLocation)
    redirect_to_url();
});

