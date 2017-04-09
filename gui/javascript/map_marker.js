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
        var name, restaurantType, address, phone, rating, review_count;
        var restaurant_html = '';
        var restaurant_detail = '';
        console.log(data['features']);
        
        for(var i=0; i < data['features'].length; i++)
        {
            name = data['features'][i]['properties']['name'];
            restaurantType = data['features'][i]['properties']['restaurant_type'];
            rating = data['features'][i]['properties']['review_rating'];
            review_count = data['features'][i]['properties']['review_count'];
            phone = data['features'][i]['properties']['telephone'];
            address = data['features'][i]['properties']['address'];
            URL = data['features'][i]['properties']['url'];
            restaurant_detail = restaurant_detail +'<div class="modal fade" id="restaurantModal'+ i +'" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true"><div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header"><h5 class="modal-title" id="exampleModalLabel">'+ name +'</h5><button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>'+
            '<div class="modal-body">'+
            '<b>Type: </b>'+ restaurantType +'<br>'+
            '<b>Rating: </b>'+ rating +' of 5 ('+review_count+' reviews)<br>'+
            '<b>Address: </b>'+ address +'<br>'+ 
            '<b>Telephone: </b>'+ phone +'<br>'+ 
            '</div><div class="modal-footer"><button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button></div></div></div></div>';
            restaurant_html = restaurant_html +
            "<div class='card w-100'>" +
              "<div class='card-block'>" + 
                "<h4 class='card-title'>" + name + "</h4>" + 
                "<p class='card-text'>" + restaurantType + "</p>" + 
                "<button type='button' class='btn btn-primary' data-toggle='modal' data-target='#restaurantModal" + i + "'>Detail</button>" +  
              "</div>" + 
            "</div><br>";  
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
        $("#modalCollection").html('');
        $("#modalCollection").html(restaurant_detail);
    });
}