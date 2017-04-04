// initialize the map
var southWest = L.latLng(52.29,4.73);
var northEast = L.latLng(52.42,4.98);
var bounds = L.latLngBounds(southWest, northEast)
var default_map = L.tileLayer('http://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="http://cartodb.com/attributions">CartoDB</a>',
  subdomains: 'abcd',
  minZoom: 0,
  maxZoom: 20,
  ext: 'png'
});
var map = L.map('map', {
  maxBounds: bounds,
  layers: default_map,
  zoomControl: false,
}).setView([52.3702, 4.8952], 13);

L.control.zoom({
  position: 'topright'
}).addTo(map);

var options = {
  url: 'food.json',
  getValue: "name",
  list: { 
    match: {
      enabled: true
    },
    onKeyEnterEvent : function() {
      alert("query to ES!");
    }
  },
  theme: "square"
};

$("#countries").easyAutocomplete(options);
var sidebar = L.control.sidebar('sidebar').addTo(map);
