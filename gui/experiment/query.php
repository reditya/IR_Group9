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
				"query"=> [
					"filtered"=> [
						"query"=> [
							"match"=> [
								"food"=> $food
							]
						],
						'filter' => [
							'range' => [
								'createdTime' => [
									'gte' => 400,
									'lte' => 800
								]
							]
						]
					]
				]
			]
		];

		/*$params = [
                    'type' => 'post',
                    'body' => [
                        'size' => '10000',
                        'query' => [
				'filtered' => [
					'query' => [
						'match' => [
                                        		'food' => $food
                                		]
					],
					'filter' => [
                                        		'script' => [
                                                		'inline' => "doc['createdTime'].getHourOfDay() >= min && doc['createdTime'].getHourOfDay() <= max",
                                                        	'params' => [
                                                        		'min' => 8,
                                                                	'max' => 10
                                                       		]
                                               	 	]
						]
				]
			]	
                    ]
                ];*/
		// $params = [
  //                   'type' => 'post',
  //                   'body' => [
  //                       'size' => '10000',
  //                       'query' => [
  //                       	'match' => [
		// 						'food' => $food           	
  //                               ]
  //                       ]
  //                   ]
  //               ];
		
		// instagram
		$params['index'] = 'instagram';
		//die(json_encode($params));
		$instagram_results = $client->search($params);
		file_put_contents('clustering/ES_instagram.json', json_encode($instagram_results));
		// tweets
		$params['index']  = 'english_tweets';
		$params['type'] = 'tweet';
		$twitter_results = $client->search($params);
		//echo (json_encode($twitter_results));
		file_put_contents('clustering/ES_english_tweets.json', json_encode($twitter_results));
		exec('python clustering/food_term_cluster.py "'.$food.'" clustering/ES_english_tweets.json clustering/ES_instagram.json clustering/points.geojson clustering/clusters.geojson');
		//die('no error 2!!!!!');
		$points = json_decode(file_get_contents('clustering/points.geojson'), true);
		$clusters = json_decode(file_get_contents('clustering/clusters.geojson'), true);
	
		$merge = [
			'points' => $points,
			'clusters' => $clusters
		];
		
		echo json_encode($merge);	
		/*
		$ar_results = array_merge($instagram_results['hits']['hits'], $twitter_results['hits']['hits']);
		$coordinate = array();
		foreach($ar_results as $i)
		{
			//print_r($i['_source']);
			$coordinate[] = array($i['_source']['coordinate']['lat'], $i['_source']['coordinate']['lon']);
		}
		echo json_encode($coordinate);
		*/
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
			$recipes[] = array('title' => $r['title'], 'description' => $r['description']);
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
			//print_r($r);
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
?>
