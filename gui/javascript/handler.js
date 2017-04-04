var popup = L.popup();

function onMapClick(e) {
  popup
      .setLatLng(e.latlng)
      .setContent("You clicked the map at " + e.latlng.toString())
      .openOn(map);
}

map.on('click', onMapClick);