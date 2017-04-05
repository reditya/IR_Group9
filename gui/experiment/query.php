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
		    'type' => 'post',
		    'body' => [
		        'size' => '10000',
		        'query' => [
		        	'match' => [
		        		'food' => $food
		        	]
		        ]
		    ]
		];

		// instagram
		$params['index'] = 'instagram';
		$results = $client->search($params);
		file_put_contents('clustering/ES_instagram.json', json_encode($results));

		// tweets
		$params['index']  = 'english_tweets';
		$params['type'] = 'tweet';
		$results = $client->search($params);
		file_put_contents('clustering/ES_english_tweets.json', json_encode($results));
		exec('python clustering/food_term_cluster.py "pizza" clustering/ES_english_tweets.json clustering/ES_instagram.json clustering/tweets.geojson clustering/instagram.geojson', $output);

		//print_r($output);

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
		        	'match' => [
		        		'title' => $food
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
			$recipes[] = array('title' => $r['title'], '');
		}

		echo json_encode($recipes);	

	}

	// query for recipes detail
	else if($query == "recipesDetail")
	{
		$food = $_GET['food'];
		$params = [
		    'index' => 'english_recipes',
		    'type' => 'recipe',
		    'body' => [
		        'size' => '10',
		        'query' => [
		        	'match' => [
		        		'title' => $food
		        	]
		        ]
		    ]
		];

		$results = $client->search($params);
		$ar_results = $results['hits']['hits'];

		//print_r($ar_results);

		$output = "";
		$counter = 0;

		foreach($ar_results as $i)
		{
			$r = $i['_source'];
			// print_r($r);
			// create a div class of modal
			$output = $output . '<div class="modal fade" id="recipeModal' . $counter . '" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
								  <div class="modal-dialog" role="document">
								    <div class="modal-content">
								      <div class="modal-header">
								        <h5 class="modal-title" id="exampleModalLabel">' . $r['title'] . '</h5>
								        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
								          <span aria-hidden="true">&times;</span>
								        </button>
								      </div>
								      <div class="modal-body">
								      	' . $r["step_by_step"] . '
								      </div>
								      <div class="modal-footer">
								        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
								      </div>
								    </div>
								  </div>
								</div>';
			$counter++;
		}		
		echo $output;
	}
?>
