<?php
	// query for list of recipes
	require '../vendor/autoload.php';

	use Elasticsearch\ClientBuilder;

	$client = Elasticsearch\ClientBuilder::create()
	    ->setHosts(["54.171.151.130:9200"])
	    ->setRetries(0)
	    ->build();
	
	$params = [
	    'index' => 'restaurants',
	    'type' => 'restaurant',
	    'body' => [
	        'query' => [
	          "match_all" => new \stdClass()
	        ]
	    ]
	];

	$results = $client->search($params);
	print_r($results);
?>