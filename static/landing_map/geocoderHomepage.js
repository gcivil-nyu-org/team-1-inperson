document.onreadystatechange = function () {
    const state = document.readyState
    if (state === 'complete') {
        $('.loading').fadeOut();
    }
}

function redirect_to_map(x,y){
    $('.loading').fadeIn();
    pageURL = `/home/?radiusRange=0.5&currentlyAccessible=true&currentlyInaccessibleCheck=true&rampsCheck=true&poleCheck=true&sidewalkCheck=true&x-co=${x}&y-co=${y}`
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
