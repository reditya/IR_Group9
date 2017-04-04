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

	$result = $client->search($params);

	// Rewrite to GEOJSON
	$geoJson = [
		'type' => 'FeatureCollection',
		'features' => []
	];
	foreach($result['hits']['hits'] as $hit) {
		$geoJson['features'][] = [
			'geometry' => [
                        	'type' => 'Point',
                        	'coordinates' => [
                                	$hit['_source']['location']['lon'],
                                	$hit['_source']['location']['lat'] 
                        	]
               		 ],
			'type' => 'Feature',
			'properties' => [
				'name' => $hit['_source']['name'],
				'category' => $hit['_source']['category']
			]
		];
	}


	echo json_encode($geoJson);	
	
} else {
	$return = [
    		'error' => 'Parameter missing.',
	];
	echo json_encode($return);
}
?>
