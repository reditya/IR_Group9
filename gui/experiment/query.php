<?php
	// query for list of recipes
	require '../vendor/autoload.php';

	use Elasticsearch\ClientBuilder;

	$client = Elasticsearch\ClientBuilder::create()
	    ->setHosts(["54.171.151.130:9200"])
	    ->setRetries(0)
	    ->build();

	$query = $_GET['query'];
	
	// query for food
	if($query == "food")
	{
		$food = $_GET['food'];

		$params = [
		    'index' => 'instagram',
		    'type' => 'post',
		    'body' => [
		        'size' => '10000',
		        'query' => [
		        	'bool' => [
		        		'filter' => [
		        			'term' => ['food' => $food],
		        		]
		        	]
		        ]
		    ]
		];

		$results = $client->search($params);
		$ar_results = $results['hits']['hits'];

		$coordinate = array();
		foreach($ar_results as $i)
		{
			//print_r($i['_source']);
			$coordinate[] = array($i['_source']['coordinate']['lat'], $i['_source']['coordinate']['lon']);
		}

		echo json_encode($coordinate);
	}

	// query for recipes
	else if($query == "recipes")
	{
		$food = $_GET['food'];
		$params = [
		    'index' => 'english_recipes',
		    'type' => 'recipe',
		    'body' => [
		        'size' => '10',
		        'query' => [
		        	'bool' => [
		        		'filter' => [
		        			'term' => ['title' => $food],
		        		]
		        	]
		        ]
		    ]
		];

		$results = $client->search($params);
		$ar_results = $results['hits']['hits'];

		//print_r($ar_results);

		$recipes = array();

		foreach($ar_results as $i)
		{
			$r = $i['_source'];
			$recipes[] = array(
							'title' => $r['title']);
		}

		echo json_encode($recipes);	

	}
?>
