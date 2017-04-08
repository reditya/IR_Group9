var markerGroup = L.layerGroup().addTo(map);
var restaurantGroup = L.layerGroup().addTo(map);
var icon1 = L.icon({
    iconUrl: 'http://www.freeiconspng.com/uploads/pink-restaurants-icon-19.png',
    iconSize:     [40,50], // size of the icon
    iconAnchor:   [20,45], // point of the icon which will correspond to marker's location
    popupAnchor:  [0,-10] // point from which the popup should open relative to the iconAnchor
});

var icon2 = L.icon({
    iconUrl: 'https://cdn4.iconfinder.com/data/icons/home3/102/Untitled-12-512.png',
    iconSize:     [40,50], // size of the icon
    iconAnchor:   [20,45], // point of the icon which will correspond to marker's location
    popupAnchor:  [0,-10] // point from which the popup should open relative to the iconAnchor
});

var icon3 = L.icon({
    iconUrl: 'https://cdn4.iconfinder.com/data/icons/location-vol-4/128/location-03-512.png',
    iconSize:     [40,50], // size of the icon
    iconAnchor:   [20,45], // point of the icon which will correspond to marker's location
    popupAnchor:  [0,-10] // point from which the popup should open relative to the iconAnchor
});


// attaching function on map click and drag
map.on('click', onMapClick);
// Script for adding marker on map click
function onMapClick(e) {
    markerGroup.clearLayers();
    var marker;
    var geojsonFeature = {
        "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Point",
                "coordinates": [e.latlng.lat, e.latlng.lng]
        }
    }
    L.geoJson(geojsonFeature, { 
        pointToLayer: function(feature, latlng){
            marker = L.marker(e.latlng, {
                title: "Resource Location",
                alt: "Resource Location",
                riseOnHover: true,
                draggable: true,
            }).bindPopup("Your Selected Location");
            marker.on("popupopen", onPopupOpen);
            marker.on('dragend', function(e) {
                console.log('marker dragend event');
                populateRestaurants(marker.getLatLng().lat, marker.getLatLng().lng);
            });
            return marker;
        }
    }).addTo(markerGroup);
    populateRestaurants(e.latlng.lat, e.latlng.lng);
}

// Function to handle delete as well as other events on marker popup open
function onPopupOpen() {
    var tempMarker = this;

    // To remove marker on click of delete
    //$(".marker-delete-button:visible").click(function () {
        //getAllMarkers();
    //});
}

function onEachFeature(feature, layer) {
    // does this feature have a property named popupContent?
    if (feature.properties && feature.properties.name) {
        layer.bindPopup(feature.properties.name);
    }
}

// Populate restaurants data into sidebar
function populateRestaurants(lat, lng){
    restaurantGroup.clearLayers();
    $.get("http://176.34.152.42/gui/getRestaurants.php?range=1km&lat=" + lat + "&lon=" + lng + "&size=10", function(data, status) {
        var restaurant_html = '';
        for(var i=0; i < data['features'].length; i++)
        {
            restaurant_html = restaurant_html + '<div class="card w-100"><div class="card-block"><h3 class="card-title">'
                + data['features'][i]['properties']['name'] + '</h3><p class="card-text">'
                + data['features'][i]['properties']['restaurant_type'] + '</p><a href="#" class="btn btn-primary">Detail</a></div></div>';
            console.log(data['features'][i]);
            L.geoJson(data, {
                pointToLayer: function(feature, latlng) {
                    return L.marker(latlng, {
                        icon: icon1
                    });
                },
                onEachFeature: onEachFeature
            }).addTo(restaurantGroup);
        }
        
        $("#restaurant_cards").html('');
        $("#restaurant_cards").html(restaurant_html);
    });
}