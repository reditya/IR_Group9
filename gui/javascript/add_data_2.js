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
    L.tileLayer('http://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="http://cartodb.com/attributions">CartoDB</a>',
      subdomains: 'abcd',
      minZoom: 0,
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
      
        geojsonMarkerOptions.fillColor = color_clust[Math.floor(feature.properties.cluster)-1];
        return L.circleMarker(latlng, geojsonMarkerOptions).setRadius(4);
      },
          onEachFeature: onEachFeature_insta 
    }).addTo(map);
  }


  function show_cluster(data){
    // Find number of clusters and create array of points with in clusters
    var nb_clust = data['features'].map(function(value, index) {return value['properties']['cluster']});
    var n = []; 
    for(var i = 0; i < nb_clust.length; i++) 
    {
      if (n.indexOf(nb_clust[i]) == -1) n.push(nb_clust[i]);
    }
    nb_clust = n.length
    console.log(nb_clust)
    var cluster_list = new Array(nb_clust);
    //console.log(nb_clust);
    color_clust = [];
    // Associate random colors to clusters
    for (i = 0; i < nb_clust; i++) {
      // Random color '#'+Math.floor(Math.random()*16777215).toString(16);
      color_clust.push('#'+Math.floor(Math.random()*16777215).toString(16));
      cluster_list[i] = new Array;
    }

    // var hull = turf.convex(data);
    //L.geoJson(hull).addTo(map);
    //  L.polygon(hull).addTo(map);    
    alert("haha23456");
    L.geoJson(data, {
      pointToLayer: function (feature, latlng) {  
        cluster_list[Math.floor(feature.properties.cluster)-1].push([latlng.lng , latlng.lat]);
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
     // var hull = turf.convex(collection_cluster[d]);     
      //var h = turf.concave(collection_cluster[d],1,'miles');
      //console.log(collection_cluster[d]);
      var h = turf.convex(collection_cluster[d]);      
      h['geometry']['type'] = "LineString";
      //console.log(h['geometry']['coordinates'][0]);
      h['geometry']['coordinates'] = h['geometry']['coordinates'][0];
      console.log(h);
      h = turf.bezier(h);
      h = lineToPolygon(h);

      console.log(h);

      L.geoJson(h,{
        style: function(feature) {
          return {
            color: color_clust[d],
            weight: 0.2,
            fillOpacity: 0.5
          };       
        }
      }).addTo(map);
    }
  }

  
  
  // Instagram data    
  
  $.getJSON("test_mix_data.geojson",function(data){
    add_base_map();
    show_cluster(data);          
    //map_points_insta(data);
  })
  
  // Foursquare data
  /*
  $.getJSON("all_resto_geojson_k2_f1.geojson",function(data){
    add_base_map();
    show_cluster(data);          
    map_points_fours(data);

  })
  */
function areIdentical(a,b) {
  return a.length === b.length && a.every(function(v,i) {
    return v === b[i];
  });
}

// accepts a Feature with a or just a LineString geometry.
function lineToPolygon(f) {
  var geometry, firstVertex, lastVertex;

  if (f.type === 'Feature'){
    geometry = f.geometry;
  } else {
    geometry = f;
  }

  if (geometry.type !== 'LineString') {
    throw new Error('Only Linestring geometry type is supported.');
  }

  if (geometry.coordinates.length === 0) {
    throw new Error('Empty geometry.');
  }

  firstVertex = geometry.coordinates[0];
  lastVertex = geometry.coordinates[geometry.coordinates.length - 1];

  if (!areIdentical(firstVertex, lastVertex)) geometry.coordinates.push(firstVertex);

  if (geometry.coordinates.length < 4) {
    throw new Error('A Polygon needs to have 4 or more positions.')
  }

  geometry.type = 'Polygon';
  geometry.coordinates = [geometry.coordinates];

  return f;
};
