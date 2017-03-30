  // initialize the map
  var southWest = L.latLng(52.29,4.73);
  var northEast = L.latLng(52.42,4.98);
  var bounds = L.latLngBounds(southWest, northEast)
  var map = L.map('map', {
    maxBounds: bounds
  }).setView([52.3702, 4.8952], 13);


  var geojsonMarkerOptions = {
      radius: 8,
      fillColor: "#ff7800",
      color: "#000",
      weight: 1,
      opacity: 1,
      fillOpacity: 0.8
  };

  


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
  
    var food = feature.properties.category;
    var list = '<ul class="myList"><li><a>' + food.join('</a></li><li>') + '</li></ul>';
    layer.bindPopup(list);
  }

  function onEachFeature_fours(feature, layer) {
    
    if (feature.properties.category) {
      layer.bindPopup(feature.properties.category);
    }   
  }


  function map_points_fours(data){
    // Points
      L.geoJson(data, {
      pointToLayer: function (feature, latlng) {   
      
        geojsonMarkerOptions.fillColor = color_clust[Math.floor(feature.properties.cluster)-1];
        return L.circleMarker(latlng, geojsonMarkerOptions);
      },
          onEachFeature: onEachFeature_fours 
    }).addTo(map);
  }

  function map_points_insta(data){
    // Points
      L.geoJson(data, {
      pointToLayer: function (feature, latlng) {   
        if (feature.properties.category.length != 0){
          geojsonMarkerOptions.fillColor = color_clust[Math.floor(feature.properties.cluster)-1];
          return L.circleMarker(latlng, geojsonMarkerOptions);
        }
        
      },
          onEachFeature: onEachFeature_insta 
    }).addTo(map);
  }


  function prepare_cluster_color(data){
    // Find number of clusters and create array of points with in clusters
    nb_clust = data['features'].map(function(value, index) {return value['properties']['cluster']});
    var n = []; 
    for(var i = 0; i < nb_clust.length; i++) 
    {
      if (n.indexOf(nb_clust[i]) == -1) n.push(nb_clust[i]);
    }
    nb_clust = n.length
    console.log(nb_clust)
    cluster_list = new Array(nb_clust);
    //console.log(nb_clust);
    color_clust = [];
    // Associate random colors to clusters
    for (i = 0; i < nb_clust; i++) {
      // Random color '#'+Math.floor(Math.random()*16777215).toString(16);
      color_clust.push('#'+Math.floor(Math.random()*16777215).toString(16));
      cluster_list[i] = new Array;
    }
    

    
  }

  function show_cluster(data){
    
    // var hull = turf.convex(data);
    //L.geoJson(hull).addTo(map);
    //  L.polygon(hull).addTo(map);  
     
    L.geoJson(data, {
      filter: function (feature, layer) {  
        //console.log(feature.geometry.coordinates[0][0][0])
        cluster_list[Math.floor(feature.properties.cluster)-1].push([feature.geometry.coordinates[0][0][0][0],feature.geometry.coordinates[0][0][0][1]],[feature.geometry.coordinates[0][0][1][0],feature.geometry.coordinates[0][0][0][1]],[feature.geometry.coordinates[0][0][1][0],feature.geometry.coordinates[0][0][1][1]],[feature.geometry.coordinates[0][0][0][0],feature.geometry.coordinates[0][0][1][1]]);
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
      L.geoJson(turf.convex(collection_cluster[d]),{
        style: function(feature) {
          return {color: color_clust[d]};       
        }
      }).addTo(map);
    }
    
  }

  
  
  // Instagram data    
  $.getJSON("new_poly_data.geojson",function(data){
    show_cluster(data);          
  })
  $.getJSON("new_mix_data.geojson",function(data){
    add_base_map();
    prepare_cluster_color(data);
    //show_cluster(data);          
    map_points_insta(data);

  })
  
  
  // Foursquare data
  /*
  $.getJSON("all_resto_geojson_k2_f1.geojson",function(data){
    add_base_map();
    show_cluster(data);          
    map_points_fours(data);

  })
  */