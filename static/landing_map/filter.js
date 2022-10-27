$(document).on('click', '.filter .dropdown-menu', function (e) {
  e.stopPropagation();
});

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
    if (rampsCheck == false && poleCheck == false && sidewalkCheck == false){
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