<?php
	require 'vendor/autoload.php';

	$hosts = '54.171.151.130:9200';

	$client = Elasticsearch\ClientBuilder::create()           // Instantiate a new ClientBuilder
	                    ->setHost($hosts)      // Set the hosts
	                    ->build();              // Build the client object

	$client = Elasticsearch\ClientBuilder::create()->build();

	$searchParams = "restaurants/_search";

	try {
	    $client->search($searchParams);
	} catch (Elasticsearch\Common\Exceptions\TransportException $e) {
	    $previous = $e->getPrevious();
	}

	echo "Test GUI";

?>