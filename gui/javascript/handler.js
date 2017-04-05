var popup = L.popup();

function onMapClick(e) {
	var latlng = e.latlng;

	popup
	.setLatLng(e.latlng)
	.setContent(fetchData(latlng.lat, latlng.lng))
	.openOn(map);
}

function fetchData(lat, lng){
	var query = 'getDetails.php?range=10km&lat=' + lat + '&lon=' + lng + '&size=5';
	$.getJSON(query, function(data) {
	})
	.success(function() { return("success"); })
	.error(function() { return("error"); });
}

map.on('click', onMapClick);