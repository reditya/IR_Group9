var popup = L.popup();

function onMapClick(e) {
  popup
      .setLatLng(e.latlng)
      .setContent(fetchData())
      .openOn(map);
}

function fetchData(){
	var query = 'http://176.34.152.42/gui/getDetails.php?range=1km&lat=52.379189&lon=4.899431&size=5';
	$.getJSON(query,function(data){
		alert("A");
		return "Success";
	});

	return "Fail";
}

map.on('click', onMapClick);
