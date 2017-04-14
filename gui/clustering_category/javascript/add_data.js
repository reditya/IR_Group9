  // initialize the map
  var southWest = L.latLng(52.29,4.73);
  var northEast = L.latLng(52.42,4.98);
  var bounds = L.latLngBounds(southWest, northEast)
  var polygonGroup = L.layerGroup().addTo(map);
  var geojsonMarkerOptions = {
      radius: 8,
      fillColor: "#ff7800",
      color: "#000",
      weight: 1,
      opacity: 1,
      fillOpacity: 0.8
  };

  
  var data_list = []

function add_base_map(){
    L.tileLayer('http://stamen-tiles-{s}.a.ssl.fastly.net/toner/{z}/{x}/{y}.{ext}', {
      attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      subdomains: 'abcd',
      minZoom: 10,
      maxZoom: 20,
      ext: 'png'
    }).addTo(map);
}

  
function onEachFeature_insta(feature, layer) {
    if (feature.properties.category.length != 0){
        var food = feature.properties.category;
        var list = '<ul class="myList"><li><a>' + food.join('</a></li><li>') + '</li></ul>';
        layer.bindPopup(list);
    }
}

function onEachFeature_fours(feature, layer) {
    if (feature.properties.category) {
        layer.bindPopup(feature.properties.category);
    }   
}

function onEachFeature_poly(feature, layer) {
    
    if (feature.properties.category) {

      if (feature.properties.category.length != 0){
    var food = feature.properties.category;
    var list = '<ul class="myList"><li><a>' + food.join('</a></li><li>') + '</li></ul>';
    layer.bindPopup(list);
    }   
    else {
          console.log(feature.properties.category)
      layer.bindPopup(feature.properties.category);
    }
  }
}

function map_points_fours(data){
    // Points
      L.geoJson(data, {
      pointToLayer: function (feature, latlng) {   
      
        geojsonMarkerOptions.fillColor = color_clust[Math.floor(feature.properties.cluster)];
        return L.circleMarker(latlng, geojsonMarkerOptions);
      },
          onEachFeature: onEachFeature_fours 
    }).addTo(map);
}

function map_points_insta(data){
    // Points
    L.geoJson(data, {
        pointToLayer: function (feature, latlng) { 
        data_list.push([latlng.lat, latlng.lng,feature.properties.intensity])  
            if (feature.properties.category.length != 0){
              geojsonMarkerOptions.fillColor = color_clust[Math.floor(feature.properties.cluster)];
              return L.circleMarker(latlng, geojsonMarkerOptions);
            }
        },
        onEachFeature: onEachFeature_insta 
    }).addTo(map);
    //console.log(data_list)
}

var nb_clust;
function prepare_cluster_color(data){
    // Find number of clusters and create array of points with in clusters
    nb_clust = data['features'].map(function(value, index) {return value['properties']['cluster']});
    bool_food_list = []
    var n = []; 
    for(var i = 0; i < nb_clust.length; i++) 
    {
      bool_food_list.push([])
      if (n.indexOf(nb_clust[i]) == -1) n.push(nb_clust[i]);
    }
    nb_clust = n.length
    //console.log(n)
    for(var i = 0; i < data['features'].length; i++) {
      //console.log(data['features'][i]['properties'])
      /*
      if (data['features'][i]['properties']['category'].length >0){
      console.log(data['features'][i]['properties']['category'].length )
          console.log(data['features'][i]['properties']['category'])
}*/
      if (data['features'][i]['properties']['category'].length != 0){
        bool_food_list[ Math.floor(data['features'][i]['properties']['cluster'])] = 1
      }
    } 
    //console.log(nb_clust);
    color_clust = [];
    // Associate random colors to clusters
    for (i = 0; i < nb_clust; i++) {
      // Random color '#'+Math.floor(Math.random()*16777215).toString(16);
      if (bool_food_list[i] > 0){
              color_clust.push('#'+Math.floor(Math.random()*16777215).toString(16));
      }
      else
      {
              color_clust.push('no');
      }

    }
}

  function show_cluster(data){
    cluster_list = new Array(nb_clust);
    collection_cat = new Array(nb_clust);
    polygonGroup.clearLayers();
    for (i = 0; i < nb_clust; i++) {
      // Random color '#'+Math.floor(Math.random()*16777215).toString(16);
      cluster_list[i] = new Array;
      collection_cat[i] = new Array;
    }
    console.log(nb_clust);
    // var hull = turf.convex(data);
    //L.geoJson(hull).addTo(map);
    //  L.polygon(hull).addTo(map);  
 
    L.geoJson(data, {
      filter: function (feature, layer) {  
       
        if (feature.properties.category.length > 0 && collection_cat[Math.floor(feature.properties.cluster)].length <= 0){
                    collection_cat[Math.floor(feature.properties.cluster)].push(feature.properties.category)

        } 

        cluster_list[Math.floor(feature.properties.cluster)].push([feature.geometry.coordinates[0][0][0][0],feature.geometry.coordinates[0][0][0][1]],[feature.geometry.coordinates[0][0][1][0],feature.geometry.coordinates[0][0][0][1]],[feature.geometry.coordinates[0][0][1][0],feature.geometry.coordinates[0][0][1][1]],[feature.geometry.coordinates[0][0][0][0],feature.geometry.coordinates[0][0][1][1]]);
      }
    })
  
    collection_cluster = new Array(nb_clust);
    for (i = 0; i < nb_clust; i++) {
      test = [];
      for (d in cluster_list[i]){
          test.push(turf.point(cluster_list[i][d]))
      }
      collection_cluster[i] = turf.featurecollection(test)
    }
     // Polygons
    for (d in collection_cluster){   
      //console.log((collection_cluster[d]))
     // var hull = turf.convex(collection_cluster[d]);  
     
        if (color_clust[d] != 'no'){
            a = turf.convex(collection_cluster[d])
            a.properties.category = collection_cat[d]
            L.geoJson(a,{
                style: function(feature) {
                    return {color: color_clust[d]};       
                },
                onEachFeature: onEachFeature_poly
            }).addTo(polygonGroup);
        }
    }
}

  function show_cluster_max(data){

    cluster_list = new Array(nb_clust);
    for (i = 0; i < nb_clust; i++) {
      // Random color '#'+Math.floor(Math.random()*16777215).toString(16);
      cluster_list[i] = new Array;
    }
    // var hull = turf.convex(data);
    //L.geoJson(hull).addTo(map);
    //  L.polygon(hull).addTo(map);  
     
    L.geoJson(data, {
      filter: function (feature, layer) {  
        //console.log(feature.geometry.coordinates[0][0][0])
        cluster_list[Math.floor(feature.properties.cluster)].push([feature.geometry.coordinates[0][0][0][0],feature.geometry.coordinates[0][0][0][1]],[feature.geometry.coordinates[0][0][1][0],feature.geometry.coordinates[0][0][0][1]],[feature.geometry.coordinates[0][0][1][0],feature.geometry.coordinates[0][0][1][1]],[feature.geometry.coordinates[0][0][0][0],feature.geometry.coordinates[0][0][1][1]]);
      }
    })
  
    polygonGroup.clearLayers();    
    collection_cluster = new Array(nb_clust);
    for (i = 0; i < nb_clust; i++) {
      test = [];
      for (d in cluster_list[i]){
          test.push(turf.point(cluster_list[i][d]))
      }
      collection_cluster[i] = turf.featurecollection(test)
    }
     // Polygons
    for (d in collection_cluster){      
      //console.log((collection_cluster[d]))
     // var hull = turf.convex(collection_cluster[d]);     
      L.geoJson(turf.convex(collection_cluster[d]),{
        onEachFeature: onEachFeature_poly,
        style: function(feature) {
          return {color: color_clust[d]};       
        }
      }).addTo(polygonGroup);
    }
    
  }
  

  function show_heatmap(data){
    /*
    L.geoJson(data, {
      pointToLayer: function (feature, latlng) {   
        if (feature.properties.category.length != 0){
          geojsonMarkerOptions.fillColor = color_clust[Math.floor(feature.properties.cluster)];
          return L.circleMarker(latlng, geojsonMarkerOptions);
        }
        
      },
          onEachFeature: onEachFeature_insta 
    }).addTo(map);
  */
    var heat = L.heatLayer(data_list, {radius: 30, maxZoom: 15}).addTo(map);
  }


/*
// Heatmap
  // For one specific food term
  $.getJSON("new_point.geojson",function(data){
    add_base_map();
    prepare_cluster_color(data);
    map_points_insta(data);
    show_heatmap(data)

    //show_cluster(data);          

  })
*/

  // Instagram data    
  
  
  // All categories
/*  $.getJSON("new_point.geojson",function(data){
    add_base_map();
    prepare_cluster_color(data);
    console.log("cluster prepared")
    //show_cluster(data);          

  })
  $.getJSON("new_poly.geojson",function(data){
    show_cluster(data);          
    console.log("clster shown")    
  })

    $.getJSON("new_point.geojson",function(data){
          map_points_insta(data);
          console.log("points shown")
})*/

  
  // Foursquare data
  /*
  $.getJSON("all_resto_geojson_k2_f1.geojson",function(data){
    add_base_map();
    show_cluster(data);          
    map_points_fours(data);

  })
  */