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
        <div id="floating-panel">
            <input id="countries" placeholder="Type food here"/>
        </div>
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
        <div id="sidebar" class="sidebar collapsed">
            <!-- Nav tabs -->
            <div class="sidebar-tabs">
                <ul role="tablist">
                    <li><a href="#home" role="tab"><i class="fa fa-bars"></i></a></li>
                    <li><a href="#profile" role="tab"><i class="fa fa-user"></i></a></li>
                </ul>
            </div>

            <!-- Tab panes -->
            <div class="sidebar-content">
                <div class="sidebar-pane" id="home">
                    <h1 class="sidebar-header">
                        Restaurant List
                        <span class="sidebar-close"><i class="fa fa-caret-left"></i></span>
                    </h1>
                </div>

                <div class="sidebar-pane" id="profile">
                    <h1 class="sidebar-header">Recipes List<span class="sidebar-close"><i class="fa fa-caret-left"></i></span></h1>
                    <span id='span_recipes'>

                    </span>                
                </div>

            </div>
        </div>
        <div class="map" id="map"></div>

    <script src="javascript/add_data_2.js"></script>
    <script src="http://code.jquery.com/jquery-1.12.3.min.js"></script>
    <script src="javascript/jquery.easy-autocomplete.min.js"></script>    
    <script src="javascript/feedback.js"></script>
    <script src="javascript/handler.js"></script>
    <script src="javascript/leaflet.customsearchbox.min.js"></script>
    <script src="javascript/leaflet-sidebar.js"></script>
</body>
</html>