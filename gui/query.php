<?php
	// query for list of recipes
	require '../vendor/autoload.php';
	use Elasticsearch\ClientBuilder;

	function dateFilter($data, $starts, $ends){
		$tempData = json_decode($data, true);
		$upperHits = $tempData['hits'];
		$hits = $tempData['hits']['hits'];
		$max = 0;
			
		$filtered = [];
		foreach($hits as $hit) {
			$source = $hit['_source'];
			$date = intval($source['createdTime']);
			$hours = intval(date('H', $date));
		
			if ($hours >= $starts && $hours <= $ends){
				if ($val['_score'] > $max) {
					$max = $val['_score'];
				}

				$filtered[] = $hit;
			}
		}

		$upperHits['total'] = count($filtered);
		$upperHits['hits'] = array_values($filtered);
		$upperHits['max_score'] = $max;

		$tempData['hits'] = $upperHits;
		return json_encode($tempData);
	}

	$client = Elasticsearch\ClientBuilder::create()
	    ->setHosts(["54.171.151.130:9200"])
	    ->setRetries(0)
	    ->build();
	$query = $_GET['query'];
	$start = $_GET['start'];
	$end = $_GET['end'];

	$ret = [];

	// query for food
	if($query == "food")
	{	
		$food_list = $_GET['food'];
		$food_list = explode(',', $food_list);
		foreach($food_list as $food) {
			$params = [
				'type' => 'post',
				'body' => [
					'size' => '10000',
					'query'=> [
						'filtered' => [
							'query' => [
								'match' => [
									'food' => $food
								]
							]
						]
					]
				]
			];
		
			// instagram
			$params['index'] = 'instagram';
			$instagram_results = $client->search($params);
			$insta_json = dateFilter(json_encode($instagram_results), $start, $end);
			file_put_contents('clustering/ES_instagram.json', $insta_json);
			
			// tweets
			$params['index']  = 'english_tweets';
			$params['type'] = 'tweet';
			$twitter_results = $client->search($params);
			$twitter_json = dateFilter(json_encode($twitter_results), $start, $end);
			file_put_contents('clustering/ES_english_tweets.json', $twitter_json);
			
			exec('python clustering/food_term_cluster.py "'.$food.'" clustering/ES_english_tweets.json clustering/ES_instagram.json clustering/points.geojson clustering/clusters.geojson');
			
			$points = json_decode(file_get_contents('clustering/points.geojson'), true);
			$clusters = json_decode(file_get_contents('clustering/clusters.geojson'), true);
	
			$ret['points'][$food] = $points;
			$ret['clusters'][$food] = $clusters;
		}
		
		echo json_encode($ret);
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
		        ],
		        'sort' => [
		        	"_score" => ["order" => "desc"],
		        	"rating" => ["order" => "desc"]
		        ]
		    ]
		];
		$results = $client->search($params);
		$ar_results = $results['hits']['hits'];
		
		$recipes = array();
		foreach($ar_results as $i)
		{
			$r = $i['_source'];
			$recipes[] = array('title' => $r['title'], 'description' => $r['description'], 'rating' => $r['rating']);
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
		        ],
		        'sort' => [
		        	"_score" => ["order" => "desc"],
		        	"rating" => ["order" => "desc"]
		        ]
		    ]
		];
		
		$results = $client->search($params);
		$ar_results = $results['hits']['hits'];
		
		$output = "";
		$counter = 0;
		foreach($ar_results as $i)
		{
			$r = $i['_source'];
			
			// Logic for ingredients view
			$ingredients_div = "<b>Ingredients</b><br>";
			$ingredients = explode("|",$r['ingredients']);			
			$ingredients_div = $ingredients_div . '<table class="table table-condensed"><tbody>';
			$c = 1;
			foreach($ingredients as $j)
			{
				if($c % 2 != 0)
				{
					$ingredients_div .= "<tr><td>".$j."</td>";
				}
				else
				{
					$ingredients_div .= "<td>".$j."</td></tr>";
				}
				$c++;
			}
			$ingredients_div .= "</tbody></table>";
			// Logic for step by step view
			$step_div = "<b>How to Cook : </b><br>";
			$step = explode("|",$r['step_by_step']);			
			$step_div .= '<ol>';
			foreach($step as $j)
			{
				$step_div .= "<li>".$j."</li>";
			}
			$step_div .= "</ol>";
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
								      	<img src="http:'. $r['image_link'] .'" class="img-rounded"> <br>
								      	<b>Cooking time: </b>' . $r['finish_time'] . ' mins<br>
								      	<b>Preparation time: </b>' . $r['preparation_time'] . ' mins<br> 
								      	' . $ingredients_div . '<br>
								      	' . $step_div . '<br>
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

	else if($query == "category")
	{
		$params = [
			'type' => 'post',
			'body' => [
				'size' => '10000',
				'query'=> [
					'filtered' => [
						'query' => [
							'match_all' => new \stdClass()
						]
					]
				]
			]
		];
		
		// instagram
		$params['index'] = 'instagram';
		$instagram_results = $client->search($params);
		$insta_json = dateFilter(json_encode($instagram_results), $start, $end);
		file_put_contents('clustering_category/ES_instagram.json', $insta_json);
		
		// tweets
		$params['index']  = 'english_tweets';
		$params['type'] = 'tweet';
		$twitter_results = $client->search($params);
		$twitter_json = dateFilter(json_encode($twitter_results), $start, $end);
		file_put_contents('clustering_category/ES_english_tweets.json', $twitter_json);
		
		$food_list = $_GET['food'];
		$food_list = explode(',', $food_list);
		$ret = [];

		foreach($food_list as $food) {
			exec('python clustering_category/show_cat.py clustering_category/ES_instagram.json clustering_category/ES_english_tweets.json clustering_category/points.geojson clustering_category/polygons.geojson clustering_category/food_category.csv "'.$food.'" True');
			$points = json_decode(file_get_contents('clustering_category/points.geojson'), true);
			$clusters = json_decode(file_get_contents('clustering_category/polygons.geojson'), true);
			
			$ret['points'][$food] = $points;
			$ret['clusters'][$food] = $clusters;
		}
		
		echo json_encode($ret);
	}
?>
