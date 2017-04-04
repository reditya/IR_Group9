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
    <link rel="stylesheet" href="css/feedback.css" />
    <link rel="stylesheet" href="css/style.css" />
    <script src="leaflet/leaflet.js"></script> 
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.0/jquery.min.js"/>
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
    <script src="javascript/feedback.js"></script>
    <script src="javascript/handler.js"></script>
</body>
</html>