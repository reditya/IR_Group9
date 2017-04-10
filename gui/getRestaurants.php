<?php

/*
Mandatory parameters are: 	lon, lat, size and range
Optional parameters are:	keyword
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

	$query = [];
	if(isset($_GET['keyword'])) {
		$query = [
			'multi_match' => [
                    		'query' => $_GET['keyword'],
                    		'fields' => [
                      			'restaurant_type',
                      			'descTitle'
                    		]
                  	]
		];
	} else {
		$query = [
			'match_all' => new \stdClass()
		];
	}	

	$params = [
	    'index' => 'thuisbezorgd',
	    'type' => 'restaurant',
	    'body' => [
		'size' => $_GET['size'],
		'query' => $query,
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
	$i = 0;
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
		];
		unset($hit['_source']['location']);
		$geoJson['features'][$i]['properties'] = $hit['_source'];
		$i += 1;
	}


	echo json_encode($geoJson);	
	
} else {
	$return = [
    		'error' => 'Parameter missing.',
	];
	echo json_encode($return);
}
?>
