document.onreadystatechange = function () {
    const state = document.readyState
    if (state === 'complete') {
        $('.loading').fadeOut();
    }
}

currentLocation = {};
searchedLocation = {};
var mapLocation =  [-73.98, 40.694];

filterParams =  Object.fromEntries(new URLSearchParams(document.URL.split('?')[1]));

if(Object.keys(filterParams).length != 0){
    mapLocation = [ JSON.parse(filterParams['x-co']), JSON.parse(filterParams['y-co'])]
    searchedLocation['longitude'] = JSON.parse(filterParams['x-co']);
    searchedLocation['latitude'] = JSON.parse(filterParams['y-co']);
}
else {
    getLocation();
}

function highlight_card(infraID) {
    $(".well").removeClass("highlight-card")
    console.log("INFRA ID: ", infraID);
    const el = document.getElementById(infraID);
    $('#' + infraID).addClass("highlight-card")
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
      },
    bbox: [-74.103684, 40.527645, -73.619187, 40.940556],
    countries: 'US',
});

geocoder.addTo('#geocoder-low-vision');

geocoder.on('result', (e) => {
    searchedLocation['longitude'] = e.result.geometry.coordinates[0];
    searchedLocation['latitude'] = e.result.geometry.coordinates[1];
    console.log("searchedLocation", searchedLocation)
    redirect_to_url();
});

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