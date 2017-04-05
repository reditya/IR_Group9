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
    var markersGeoJsonArray = markerGroup.toGeoJSON();
    coord = markersGeoJsonArray["features"][0]["features"][0]["geometry"]["coordinates"]
    lon = coord[0];
    lat = coord[1];
    console.log(coord);
    alert("coordinate : " + coord + "\nlon : " + lon + "\nlat :" + lat);
}
