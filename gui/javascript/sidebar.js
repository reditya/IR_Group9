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
  //maxBounds: bounds,
  layers: default_map,
  zoomControl: false,
}).setView([52.3702, 4.8952], 13);

L.control.zoom({
  position: 'topleft'
}).addTo(map);

// add Amsterdam border
$.getJSON("Amsterdam_AL8.GeoJson",function(data){
  var geojsonMarkerOptions = {
      fillOpacity: 0
  };

  L.geoJSON(data, geojsonMarkerOptions).addTo(map);
});

// add initial clustering
$.getJSON("initial_clustering.geojson",function(data){
  var geojsonMarkerOptions = {
      fillOpacity: 1
  };

  //L.geoJSON(data, geojsonMarkerOptions).addTo(map);
});

var view_html = 'Show as: <br><label class="radio-inline"><input type="radio" name="optradio1" id="heatmap_view" value="heatmap"> Heatmap </label> <label class="radio-inline"><input type="radio" name="optradio1" id="cluster_view" value="cluster"> Cluster </label>'

// ACTION FOR FOOD TERM OR CATEGORY SEARCH
var global_radio_selection = "";
var global_view_selection = "";
$('#radio_search input').on('change', function() {
   $("#layer_option").html('');
   var selected = $('input[name=optradio]:checked', '#radio_search').val();
   global_radio_selection = selected; 
   if(selected == "category")
   {
    $("#category-panel-form").show();
    $("#foodterm-panel-form").hide();
    $("#radio-view").html('');
    $("#radio-view").html(view_html);
    $('#radio-view input').on('change', function(){
        global_view_selection = $('input[name=optradio1]:checked', '#radio-view').val();
        $("#layer_option").html('');
        for(i=0; i<pointMarker.length; i++)
        {
        map.removeLayer(pointMarker[i]);
        }
    });
   }
   else if(selected == "foodterm")
   {
    $("#foodterm-panel-form").show();
    $("#category-panel-form").hide();
    $("#radio-view").html('');
    global_view_selection = "";
    polygonGroup.clearLayers();
   }
});


var pointMarker = new Array();

var sidebar = L.control.sidebar('sidebar').addTo(map);

var selectHtml = '';
selectHtml += "<select multiple id=foodSelection style='width:350px;'>";
selectHtml += "<option value=''></option>";
// chosen select panel

$.getJSON("food.json", function(data){
  for(i=0; i<data.length; i++)
  {
    //console.log(data[i]);
    selectHtml += "<option value='" + data[i]['name'] + "'" + ">" + data[i]['name'] + "</option>";
  }
  selectHtml += "</select>";
  $("#foodterm-panel-form").append(selectHtml);
  $("#foodSelection").chosen({ max_selected_options: 5});
  $("#foodterm-panel-form").hide();
});

var selectCategory = '';
selectCategory += "<select multiple id=categorySelection style='width:350px;'>";
selectCategory += "<option value=''></option>";
// chosen select panel

$.getJSON("category.json", function(data){
  for(i=0; i<data.length; i++)
  {
    //console.log(data[i]);
    selectCategory += "<option value='" + data[i]['name'] + "'" + ">" + data[i]['name'] + "</option>";
  }
  selectCategory += "</select>";
  $("#category-panel-form").append(selectCategory);
  $("#categorySelection").chosen({ max_selected_options: 5});
  $("#category-panel-form").hide();
});

var foodterm = "";
$('#buttonSearch').on('click', function(e) {
    search();
});

function search(){
    var hour1 = document.getElementById("hour1Temp").value;
    var hour2 = document.getElementById("hour2Temp").value;
    foodterm = "";
    $("#layer_option").html('');
    if(global_radio_selection == "foodterm"){
        foodterm = $("#foodSelection").val(); 
        if (foodterm == null){
        }
        else{
            console.log(foodterm);
            searchPoints(hour1,hour2);
        }   
    }else if (global_radio_selection == "category"){
        foodterm = $("#categorySelection").val();
        if (foodterm == null){
        }
        else{
            if (global_view_selection == "heatmap"){
                polygonGroup.clearLayers();
                searchCategory(hour1,hour2);
            }else if(global_view_selection == "cluster"){
                console.log(foodterm);
                var category = foodterm;
                if (category == "alcoholic beverage"){
                    category = "alcohol";
                }else if(category == "non-alcoholic beverage"){
                    category = "non_alcohol";
                }else if(category == "fast-food"){
                    category = "fast";
                }
                clusterCategory(category);
            }
        }
    }
}

function clusterCategory(category){
    var pointfile = "clustering_category/new_point_"+category+".geojson";
    var polyfile = "clustering_category/new_poly_"+category+".geojson";
    $.getJSON(pointfile,function(data){
      prepare_cluster_color(data);
      $.getJSON(polyfile,function(data){
        show_cluster(data);    
      });
    });
}

var heat_dict;

function searchPoints(start, end){
if (start > 23){
	start = 23;
}  
$("#loading-panel").show();
  for(i=0; i<pointMarker.length; i++)
  {
    map.removeLayer(pointMarker[i]);
  }

  //var foodterm = $("#countries").getSelectedItemData().name;
  foodterm = $("#foodSelection").val();  
  var geojsonMarkerOptions = {
    radius: 8,
    fillColor: "#ff7800",
    color: "#000",
    weight: 1,
    opacity: 1,
    fillOpacity: 0.8
  };

  //alert(foodterm);

  // this needs to be changed
  var food_query = 'query.php?query=food&food='+foodterm+'&start='+start+'&end='+end;
  $.getJSON(food_query,function(data){
    var layer_radio = '<form id="layer_search">';
    var pointData = data['points'];
    var counter = 1;
    heat_dict = {};
    for(var key in pointData)
    {
      // add the radio button
      if(counter == 1) 
      {
        layer_radio += '<label class="radio-inline active">';
        layer_radio +=  '<input checked type="radio" name="layer_foodterm" value="' + key + '"> ' + key + ' ';
      }
      else 
      {
        layer_radio += '<label class="radio-inline">';
        layer_radio +=  '<input type="radio" name="layer_foodterm" value="' + key + '"> ' + key + ' ';        
      }
      layer_radio += '</label>';
      console.log(key);
      marker_point = L.geoJSON(pointData[key]);
      var data_heat = [];

      var datapoint = pointData[key]['features'];
      for(i=0;i<datapoint.length;i++)
      {
        //console.log(datapoint[i]);
        data_heat.push([datapoint[i]['geometry']['coordinates'][1], datapoint[i]['geometry']['coordinates'][0], datapoint[i]['properties']['intensity']]);
      }

      //console.log(data_heat);
      var heat_layer = L.heatLayer(data_heat, {radius: 30, maxZoom: 15});
      heat_dict[key] = heat_layer;
      pointMarker.push(heat_dict[key]);
      if(counter == 1) map.addLayer(heat_dict[key]);      
      counter += 1;
    }
    layer_radio += '</form>';
    $("#layer_option").html('');
    $("#layer_option").html(layer_radio);   
    $("#loading-panel").hide();

    // add javascript event
    $('#layer_search input').on('change', function() {
       var selected = $('input[name=layer_foodterm]:checked', '#layer_search').val();
       //alert(selected);
       for(i=0; i<pointMarker.length; i++)
      {
        map.removeLayer(pointMarker[i]);
      }
      console.log(selected);
      pointMarker.push(heat_dict[selected]);
      console.log(heat_dict[selected]);
      map.addLayer(heat_dict[selected]);
    });    
  });

  // recipes detail in the sidebar
  var detail_query = 'query.php?query=recipesDetail&food='+foodterm+'&start='+start+'&end='+end;
  $.get(detail_query,function(data){
    $('#modalCollection').html('');
    $('#modalCollection').html(data);
    //alert(foodterm);
    //console.log(data);
    var recipes_query = 'query.php?query=recipes&food='+foodterm+'&start='+start+'&end='+end;
    $.getJSON(recipes_query,function(data){
      //var recipes_html = '<h3>Top ' + foodterm + ' Recipes for you</h3><br>';
      var recipes_html = '<p>';
      //recipes_html = recipes_html + '<ul>';
      for(var i=0; i < data.length; i++)
      {
        recipes_html = recipes_html 
          + "<div class='card w-100'>" +
              "<div class='card-block'>" + 
                "<h4 class='card-title'>" + data[i]['title'] + " [" + data[i]['rating'] + "/5]" + "</h4>" + 
                "<p class='card-text'>" + data[i]['description'] + "</p>" + 
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

function searchCategory(start, end){
  $("#loading-panel").show();  
  for(i=0; i<pointMarker.length; i++)
  {
    map.removeLayer(pointMarker[i]);
  }

  //var foodterm = $("#countries").getSelectedItemData().name;
  foodterm = $("#categorySelection").val();  

  var geojsonMarkerOptions = {
    radius: 8,
    fillColor: "#ff7800",
    color: "#000",
    weight: 1,
    opacity: 1,
    fillOpacity: 0.8
  };

  //alert(foodterm);

  // this needs to be changed
  var food_query = 'query.php?query=category&food='+foodterm+'&start='+start+'&end='+end;
  $.getJSON(food_query,function(data){
    var layer_radio = '<form id="layer_search">';
    var pointData = data['points'];
    var counter = 1;
    heat_dict = {};
    for(var key in pointData)
    {
      // add the radio button
      if(counter == 1) 
      {
        layer_radio += '<label class="radio-inline active">';
        layer_radio +=  '<input checked type="radio" name="layer_foodterm" value="' + key + '"> ' + key + ' ';
      }
      else 
      {
        layer_radio += '<label class="radio-inline">';
        layer_radio +=  '<input type="radio" name="layer_foodterm" value="' + key + '"> ' + key + ' ';        
      }
      layer_radio += '</label>';
      console.log(key);
      marker_point = L.geoJSON(pointData[key]);
      var data_heat = [];

      var datapoint = pointData[key]['features'];
      for(i=0;i<datapoint.length;i++)
      {
        //console.log(datapoint[i]);
        data_heat.push([datapoint[i]['geometry']['coordinates'][1], datapoint[i]['geometry']['coordinates'][0], datapoint[i]['properties']['intensity']]);
      }

      //console.log(data_heat);
      var heat_layer = L.heatLayer(data_heat, {radius: 15, maxZoom: 15});
      heat_dict[key] = heat_layer;
      pointMarker.push(heat_dict[key]);
      if(counter == 1) map.addLayer(heat_dict[key]);      
      counter += 1;
    }
    layer_radio += '</form>';
    $("#layer_option").html('');
    $("#layer_option").html(layer_radio);  
    $("#loading-panel").hide(); 

    // add javascript event
    $('#layer_search input').on('change', function() {
       var selected = $('input[name=layer_foodterm]:checked', '#layer_search').val();
       //alert(selected);
       for(i=0; i<pointMarker.length; i++)
      {
        map.removeLayer(pointMarker[i]);
      }
      console.log(selected);
      pointMarker.push(heat_dict[selected]);
      console.log(heat_dict[selected]);
      map.addLayer(heat_dict[selected]);
    });    
  });

  // recipes detail in the sidebar
  var detail_query = 'query.php?query=recipesDetail&food='+foodterm+'&start='+start+'&end='+end;
  $.get(detail_query,function(data){
    $('#modalCollection').html('');
    $('#modalCollection').html(data);
    //alert(foodterm);
    //console.log(data);
    var recipes_query = 'query.php?query=recipes&food='+foodterm+'&start='+start+'&end='+end;
    $.getJSON(recipes_query,function(data){
      //var recipes_html = '<h3>Top ' + foodterm + ' Recipes for you</h3><br>';
      var recipes_html = '<p>';
      //recipes_html = recipes_html + '<ul>';
      for(var i=0; i < data.length; i++)
      {
        recipes_html = recipes_html 
          + "<div class='card w-100'>" +
              "<div class='card-block'>" + 
                "<h4 class='card-title'>" + data[i]['title'] + " [" + data[i]['rating'] + "/5]" + "</h4>" + 
                "<p class='card-text'>" + data[i]['description'] + "</p>" + 
                "<button type='button' class='btn btn-primary' data-toggle='modal' data-target='#recipeModal" + i + "'>Detail</button>" +  
              "</div>" + 
            "</div><br>";          
        //console.log(recipes_html);
        //recipes_html = recipes_html + '<li>' + data[i]['title'] + '</li>';
      }
      recipes_html = recipes_html + '</p>';
      //recipes_html = recipes_html + '</ul>';
      $("#span_recipes").html('');
      $("#span_recipes").html(recipes_html);        
    });
  });
}
