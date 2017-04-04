var popup = L.popup();

function onMapClick(e) {
  popup
      .setLatLng(e.latlng)
      .setContent(fetchData())
      .openOn(map);
}

function fetchData(){
	$.ajax(
		{
			url:"getDetails.php?range=1km&lat=52.379189&lon=4.899431&size=5", 
			type:"POST",
			contentType:"application/json; charset=utf-8",
			data:{some_string:"resturants"},
			dataType:"json",
			success:function(data){
				return('Success');
			},
			error: function() {
				return('Error occurs!');
			}
		}
	)
}

map.on('click', onMapClick);