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
  position: 'topleft'
}).addTo(map);

// add Amsterdam border
$.getJSON("Amsterdam_AL8.GeoJson",function(data){
  L.geoJSON(data).addTo(map);
});

var pointMarker = new Array();

var options = {
  url: 'food.json',
  getValue: "name",
  list: { 
    match: {
      enabled: true
    },
    onKeyEnterEvent : function() {

      for(i=0; i<pointMarker.length; i++)
      {
        map.removeLayer(pointMarker[i]);
      }

      var foodterm = $("#countries").getSelectedItemData().name;
      foodterm = foodterm.toLowerCase();

      var geojsonMarkerOptions = {
        radius: 8,
        fillColor: "#ff7800",
        color: "#000",
        weight: 1,
        opacity: 1,
        fillOpacity: 0.8
      };

      alert(foodterm);

      var food_query = 'query.php?query=food&food='+foodterm;
      $.getJSON(food_query,function(data){
        for(var i=0; i < data.length; i++)
        {
          var latlng = L.latLng(data[i][0], data[i][1]);
          marker = new L.circleMarker(latlng, geojsonMarkerOptions);
          pointMarker.push(marker);
          map.addLayer(marker);
        }
      });

      var detail_query = 'query.php?query=recipesDetail&food='+foodterm;
      $.get(detail_query,function(data){
        $('#modalCollection').html('');
        $('#modalCollection').html(data);
        console.log(data);
        var recipes_query = 'query.php?query=recipes&food='+foodterm;
        $.getJSON(recipes_query,function(data){
          //var recipes_html = '<h3>Top ' + foodterm + ' Recipes for you</h3><br>';
          var recipes_html = '<p>';
          //recipes_html = recipes_html + '<ul>';
          for(var i=0; i < data.length; i++)
          {
            recipes_html = recipes_html 
              + "<div class='card w-100'>" +
                  "<div class='card-block'>" + 
                    "<h4 class='card-title'>" + data[i]['title'] + "</h4>" + 
                    "<p class='card-text'>description of recipes here</p>" + 
                    "<button type='button' class='btn btn-primary' data-toggle='modal' data-target='#recipeModal" + i + "'>Detail</button>" +  
                  "</div>" + 
                "</div><br>";          
            console.log(recipes_html);
            //recipes_html = recipes_html + '<li>' + data[i]['title'] + '</li>';
          }
          recipes_html = recipes_html + '</p>';
          //recipes_html = recipes_html + '</ul>';
          $("#span_recipes").html('');
          $("#span_recipes").html(recipes_html);        
        });

      });
    }
  },
  theme: "square"
};

$("#countries").easyAutocomplete(options);
var sidebar = L.control.sidebar('sidebar').addTo(map);

// chosen select panel
var selectHtml = '';
selectHtml += "<select id=foodSelection style='width:350px;'>";
selectHtml += "<option value='" + "pizza" + "'" + ">" + "Pizza" + "</option>";
selectHtml += "<option value='" + "chocolate" + "'" + ">" + "Chocolate" + "</option>";
selectHtml += "<option value='" + "banana" + "'" + ">" + "Banana" + "</option>";
selectHtml += "</select>";

$("#select-panel").append(selectHtml);
$("#foodSelection").chosen();
$('#foodSelection').on('change', function(e) {
  for(i=0; i<pointMarker.length; i++)
  {
    map.removeLayer(pointMarker[i]);
  }

  //var foodterm = $("#countries").getSelectedItemData().name;
  var foodterm = $("#foodSelection").val();  
  foodterm = foodterm.toLowerCase();

  var geojsonMarkerOptions = {
    radius: 8,
    fillColor: "#ff7800",
    color: "#000",
    weight: 1,
    opacity: 1,
    fillOpacity: 0.8
  };

  alert(foodterm);

  var food_query = 'query.php?query=food&food='+foodterm;
  $.getJSON(food_query,function(data){
    for(var i=0; i < data.length; i++)
    {
      var latlng = L.latLng(data[i][0], data[i][1]);
      marker = new L.circleMarker(latlng, geojsonMarkerOptions);
      pointMarker.push(marker);
      map.addLayer(marker);
    }
  });

  var detail_query = 'query.php?query=recipesDetail&food='+foodterm;
  $.get(detail_query,function(data){
    $('#modalCollection').html('');
    $('#modalCollection').html(data);
    console.log(data);
    var recipes_query = 'query.php?query=recipes&food='+foodterm;
    $.getJSON(recipes_query,function(data){
      //var recipes_html = '<h3>Top ' + foodterm + ' Recipes for you</h3><br>';
      var recipes_html = '<p>';
      //recipes_html = recipes_html + '<ul>';
      for(var i=0; i < data.length; i++)
      {
        recipes_html = recipes_html 
          + "<div class='card w-100'>" +
              "<div class='card-block'>" + 
                "<h4 class='card-title'>" + data[i]['title'] + "</h4>" + 
                "<p class='card-text'>description of recipes here</p>" + 
                "<button type='button' class='btn btn-primary' data-toggle='modal' data-target='#recipeModal" + i + "'>Detail</button>" +  
              "</div>" + 
            "</div><br>";          
        console.log(recipes_html);
        //recipes_html = recipes_html + '<li>' + data[i]['title'] + '</li>';
      }
      recipes_html = recipes_html + '</p>';
      //recipes_html = recipes_html + '</ul>';
      $("#span_recipes").html('');
      $("#span_recipes").html(recipes_html);        
    });

  });
});