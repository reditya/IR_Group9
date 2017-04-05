var markerGroup = L.layerGroup().addTo(map);

// attaching function on map click
map.on('click', onMapClick);

// Script for adding marker on map click
function onMapClick(e) {
    markerGroup.clearLayers();
    var geojsonFeature = {
        "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Point",
                "coordinates": [e.latlng.lat, e.latlng.lng]
        }
    }

    var marker;

    L.geoJson(geojsonFeature, {
        
        pointToLayer: function(feature, latlng){
            
            marker = L.marker(e.latlng, {
                
                title: "Resource Location",
                alt: "Resource Location",
                riseOnHover: true,
                draggable: true,

            }).bindPopup("<input type='button' value='Search nearby restaurant' class='marker-search-button'/>");

            marker.on("popupopen", onPopupOpen);
       
            return marker;
        }
    }).addTo(markerGroup);

    populateRestaurants(e.latlng.lat, e.latlng.lng);
}

// Function to handle delete as well as other events on marker popup open
function onPopupOpen() {
    var tempMarker = this;

    // To remove marker on click of delete
    $(".marker-search-button:visible").click(function () {
        getAllMarkers();
    });
}

// Dummy function to test popup marker 
function getAllMarkers() {
    // Get coordinates where was clicked 
    var markersGeoJsonArray = markerGroup.toGeoJSON();
    coord = markersGeoJsonArray["features"][0]["features"][0]["geometry"]["coordinates"]
    lon = coord[0];
    lat = coord[1];
    
    // Get nearby restaurants in GeoJSON
    $.get("http://176.34.152.42/gui/getRestaurants.php?range=1km&lat=" + lat + "&lon=" + lon + "&size=10", function(data, status) {
        L.geoJSON(data).addTo(markerGroup);
    });
}

// Populate restaurants data into sidebar
function populateRestaurants(lat, lng){
    $.get("http://176.34.152.42/gui/getRestaurants.php?range=1km&lat=" + lat + "&lon=" + lng + "&size=10", function(data, status) {
        var restaurant_html = '';
        for(var i=0; i < data['features'].length; i++)
        {
          restaurant_html = restaurant_html + '<div class="card w-100"><div class="card-block"><h3 class="card-title">' 
            + data['features'][i]['properties']['name'] + '</h3><p class="card-text">'
            + data['features'][i]['properties']['category'] + '</p><a href="#" class="btn btn-primary">Button</a></div></div>';
        }
        $("#restaurant_cards").html('');
        $("#restaurant_cards").html(restaurant_html); 
    });
}