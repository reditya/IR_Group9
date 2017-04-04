var popup = L.popup();

function onMapClick(e) {
  popup
      .setLatLng(e.latlng)
      .setContent(
      	$.ajax(
	        {
	        	url:"index.php/a", 
	        	type:"POST",
	        	contentType:"application/json; charset=utf-8",
	                    data:{some_string:"resturants"},
	                    dataType:"json",
	                    success:function(data){
	                    	"Restaurants" + data;
	                    },
	                    error:function(a,b,c){

	                    }
	        }
	    ))
      .openOn(map);
}

map.on('click', onMapClick);