function redirect_to_map(x,y){
    pageURL = `/home/?radiusRange=2.75&currentlyAccessible=true&currentlyInaccessibleCheck=true&rampsCheck=true&poleCheck=true&sidewalkCheck=true&x-co=${x}&y-co=${y}`
    window.location.href = pageURL;
}

//geocoder
const geocoder = new MapboxGeocoder({
accessToken: mapboxgl.accessToken,
proximity: {
    longitude: -73.98,
    latitude: 40.694
  }
});

geocoder.addTo('#geocoder-home-page');

geocoder.on('result', (e) => {
    redirect_to_map(e.result.geometry.coordinates[0], e.result.geometry.coordinates[1]);
});
