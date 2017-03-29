<?php

require 'vendor/autoload.php';

/*$hosts = [
    // This is effectively equal to: "https://username:password!#$?*abc@foo.com:9200/"
    // [
    //     'host' => 'foo.com',
    //     'port' => '9200',
    //     'scheme' => 'https',
    //     'user' => 'username',
    //     'pass' => 'password!#$?*abc'
    // ],

    // This is equal to "http://localhost:9200/"
    [
        'host' => 'localhost',    // Only host is required
    ]
];

$client = ClientBuilder::create()           // Instantiate a new ClientBuilder
                    ->setHosts($hosts)      // Set the hosts
                    ->build();              // Build the client object

$client = Elasticsearch\ClientBuilder::create()->build();

$searchParams = "restaurants/_search";

try {
    $client->search($searchParams);
} catch (Elasticsearch\Common\Exceptions\TransportException $e) {
    $previous = $e->getPrevious();
    if ($previous instanceof 'Elasticsearch\Common\Exceptions\MaxRetriesException') {
        echo "Max retries!";
    }
}*/

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

echo $results['took'];

?>
