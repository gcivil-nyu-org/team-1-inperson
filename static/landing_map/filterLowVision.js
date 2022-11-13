$(document).on('click', '.filter .dropdown-menu', function (e) {
  e.stopPropagation();
});

document.getElementById("rangeval").innerText = document.getElementById("radiusRangeFilter").value;

if(filterParams['rampsCheck']){
    document.getElementById("rangeval").innerText = JSON.parse(filterParams['radiusRange']);
    document.getElementById("rampsCheck").checked = JSON.parse(filterParams['rampsCheck']);
    document.getElementById("poleCheck").checked = JSON.parse(filterParams['poleCheck']);
    document.getElementById("sidewalkCheck").checked = JSON.parse(filterParams['sidewalkCheck']);
    document.getElementById("currentlyInaccessibleCheck").checked = JSON.parse(filterParams['currentlyInaccessibleCheck']);
    document.getElementById("currentlyAccessibleCheck").checked = JSON.parse(filterParams['currentlyAccessible']);
    document.getElementById("radiusRangeFilter").value = JSON.parse(filterParams['radiusRange']);
}

function redirect_to_url(){
    selectedLocation = Object.keys(searchedLocation).length != 0? searchedLocation : currentLocation;
    radiusRange = document.getElementById("radiusRangeFilter").value;
    currentlyAccessible = document.getElementById("currentlyAccessibleCheck").checked;
    currentlyInaccessibleCheck = document.getElementById("currentlyInaccessibleCheck").checked;
    rampsCheck = document.getElementById("rampsCheck").checked;
    poleCheck = document.getElementById("poleCheck").checked;
    sidewalkCheck = document.getElementById("sidewalkCheck").checked;

    if (currentlyAccessible == false && currentlyInaccessibleCheck == false){
        alert("Please check atleast 1 status")
    }
    else if (rampsCheck == false && poleCheck == false && sidewalkCheck == false){
        alert("Please check atleast 1 infrastructure to display")
    }

    else{
        var params = {
            "radiusRange": radiusRange,
            "currentlyAccessible": currentlyAccessible,
            "currentlyInaccessibleCheck": currentlyInaccessibleCheck,
            "rampsCheck": rampsCheck,
            "poleCheck": poleCheck,
            "sidewalkCheck": sidewalkCheck,
            "x-co": selectedLocation['longitude'],
            "y-co": selectedLocation['latitude']
        }
        var paramString = jQuery.param(params)
        var pageUrl = document.URL.split('?')[0]+'?'+ paramString;

        window.location.href = pageUrl;
    }
}

function clear_filters(){
    document.getElementById("rampsCheck").checked = false;
    document.getElementById("poleCheck").checked = false;
    document.getElementById("sidewalkCheck").checked = false;
    document.getElementById("currentlyInaccessibleCheck").checked = false;
}

function goto_mapsPage(){
    selectedLocation = Object.keys(searchedLocation).length != 0? searchedLocation : currentLocation;
    radiusRange = document.getElementById("radiusRangeFilter").value;
    currentlyAccessible = document.getElementById("currentlyAccessibleCheck").checked;
    currentlyInaccessibleCheck = document.getElementById("currentlyInaccessibleCheck").checked;
    rampsCheck = document.getElementById("rampsCheck").checked;
    poleCheck = document.getElementById("poleCheck").checked;
    sidewalkCheck = document.getElementById("sidewalkCheck").checked;

    var params = {
            "radiusRange": radiusRange,
            "currentlyAccessible": currentlyAccessible,
            "currentlyInaccessibleCheck": currentlyInaccessibleCheck,
            "rampsCheck": rampsCheck,
            "poleCheck": poleCheck,
            "sidewalkCheck": sidewalkCheck,
            "x-co": selectedLocation['longitude'],
            "y-co": selectedLocation['latitude']
        }
    var paramString = jQuery.param(params)
    pageUrlLow = '/home/'+'?'+ paramString;

    window.location.href = pageUrlLow;
}