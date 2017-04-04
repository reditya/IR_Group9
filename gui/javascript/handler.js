var popup = L.popup();

function onMapClick(e) {
  popup
      .setLatLng(e.latlng)
      .setContent(
      	$.ajax(
	        {
	        	url:"getDetails.php?range=1km&lat=52.379189&lon=4.899431&size=5", 
	        	type:"POST",
	        	contentType:"application/json; charset=utf-8",
	                    data:{some_string:"resturants"},
	                    dataType:"json",
	                    success:function(data){
	                    	"Restaurants" + data;
	                    }
	        }
	    ))
      .openOn(map);
}

map.on('click', onMapClick);