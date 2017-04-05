<?php

/*
Parameters are: lon, lat, size and range
Return JSON
*/

require 'vendor/autoload.php';

use Elasticsearch\ClientBuilder;

header('Content-type: application/json');

if(isset($_GET['range']) && isset($_GET['lon']) && isset($_GET['lat']) && isset($_GET['size'])) {
	
	$client = Elasticsearch\ClientBuilder::create()
	    ->setHosts(["54.171.151.130:9200"])
	    ->setRetries(0)
	    ->build();

	$params = [
	    'index' => 'restaurants',
	    'type' => 'restaurant',
	    'body' => [
		'size' => $_GET['size'],
		'query' => [
		  'match_all' => new \stdClass()
		],
		'filter' => [
		  'geo_distance' => [
			'distance' => $_GET['range'],
			'location' => [
				'lat' => $_GET['lat'],
				'lon' => $_GET['lon']
			]
		  ]
		]
	    ]
	];

	$results = $client->search($params);

	echo json_encode($results);
	
} else {
	$return = [
    		'error' => 'Parameter missing.',
	];

	echo json_encode($return);
}
?>
