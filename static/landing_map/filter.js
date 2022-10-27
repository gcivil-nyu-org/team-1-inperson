$(document).on('click', '.filter .dropdown-menu', function (e) {
  e.stopPropagation();
});

const filterParams =  Object.fromEntries(new URLSearchParams(document.URL.split('?')[1]));
document.getElementById("rangeval").innerText = document.getElementById("radiusRangeFilter").value;

if(filterParams['favCheck']){
    document.getElementById("rangeval").innerText = JSON.parse(filterParams['radiusRange']);
    document.getElementById("favCheck").checked = JSON.parse(filterParams['favCheck']);
    document.getElementById("rampsCheck").checked = JSON.parse(filterParams['rampsCheck']);
    document.getElementById("poleCheck").checked = JSON.parse(filterParams['poleCheck']);
    document.getElementById("sidewalkCheck").checked = JSON.parse(filterParams['sidewalkCheck']);
    document.getElementById("currentlyInaccessibleCheck").checked = JSON.parse(filterParams['currentlyInaccessibleCheck']);
    document.getElementById("currentlyAccessibleCheck").checked = JSON.parse(filterParams['currentlyAccessible']);
    document.getElementById("radiusRangeFilter").value = JSON.parse(filterParams['radiusRange']);
}

function redirect_to_url(){
    radiusRange = document.getElementById("radiusRangeFilter").value;
    currentlyAccessible = document.getElementById("currentlyAccessibleCheck").checked;
    currentlyInaccessibleCheck = document.getElementById("currentlyInaccessibleCheck").checked;
    favCheck =  document.getElementById("favCheck").checked;
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
            "favCheck": favCheck ,
            "rampsCheck": rampsCheck,
            "poleCheck": poleCheck,
            "sidewalkCheck": sidewalkCheck
        }
    var paramString = jQuery.param(params)
    var pageUrl = document.URL.split('?')[0]+'?'+ paramString;
    console.log(pageUrl)
    sendQueryData(pageUrl, params);
    }
}

function clear_filters(){
    document.getElementById("favCheck").checked = false;
    document.getElementById("rampsCheck").checked = false;
    document.getElementById("poleCheck").checked = false;
    document.getElementById("sidewalkCheck").checked = false;
    document.getElementById("currentlyInaccessibleCheck").checked = false;
}

function sendQueryData(url, query){
        $.ajax({
          type: "GET",
          url: "/",
          data: {
              'query' : query,
              'url' : url
          },
          success: function(result){
             window.location.href = url;
          }
        });
}