<?php

// require 'vendor/autoload.php';

// use Elasticsearch\ClientBuilder;

// $client = Elasticsearch\ClientBuilder::create()
//     ->setHosts(["54.171.151.130:9200"])
//     ->setRetries(0)
//     ->build();

// $params = [
//     'index' => 'restaurants',
//     'type' => 'restaurant',
//     'body' => [
//         'query' => [
//           "match_all" => new \stdClass()
//         ]
//     ]
// ];

// $results = $client->search($params);

//echo $results['took'];

?>

<html>
<head>
    <title>A Leaflet map!</title>
    <link rel="stylesheet" href="leaflet/leaflet.css" />
    <link rel="stylesheet" href="http://netdna.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" />
    <link href="//maxcdn.bootstrapcdn.com/font-awesome/4.1.0/css/font-awesome.min.css" rel="stylesheet">
    <link rel="stylesheet" href="css/feedback.css" />
    <link rel="stylesheet" href="css/style.css" />
    <link rel="stylesheet" href="css/custom.css" />    
    <link rel="stylesheet" href="css/easy-autocomplete.min.css" />
    <link rel="stylesheet" href="css/easy-autocomplete.themes.min.css" />      
    <link rel="stylesheet" href="css/leaflet-sidebar.css" />       
    <script src="leaflet/leaflet.js"></script> 
    <script src="jquery-2.1.1.min.js"></script>
    <script src='https://npmcdn.com/@turf/turf/turf.min.js'></script>  
    <script src='https://api.mapbox.com/mapbox.js/plugins/turf/v2.0.2/turf.min.js'></script> 
</head>
<body>
    <div class="container">
        <div id="feedback">
            <div id="feedback-form" style='display:none;' class="col-xs-4 col-md-4 panel panel-default">
                <p class="feedback"><img src="images/thumb.png" height="10%"> our app?</p>
                <form method="POST" action="/feedback" class="form panel-body" role="form">
                    <label>
                        <input type="radio" name="optradio"> Yes
                    </label>
                    <label>
                        <input type="radio" name="optradio"> No
                    </label>
                </form>
            </div>
            <div id="feedback-tab">Feedback</div>
        </div>
        <div class="map" id="map"></div>
    </div>

    <script src="javascript/add_data_2.js"></script>
    <script src="http://code.jquery.com/jquery-1.12.3.min.js"></script>
    <script src="javascript/jquery.easy-autocomplete.min.js"></script>    
    <script src="javascript/feedback.js"></script>
    <script src="javascript/leaflet.customsearchbox.min.js"></script>
    <script src="javascript/leaflet-sidebar.js"></script>
    <script src="javascript/sidebar.js"></script> 
</body>
</html>