<?php

require 'vendor/autoload.php';

$hosts = [
    //This is effectively equal to: "https://username:password!#$?*abc@foo.com:9200/"
    [
        'host' => '172.31.44.39',
        'port' => '9200',
        'scheme' => 'https'
        // 'user' => 'username',
        // 'pass' => 'password!#$?*abc'
    ]

    // // This is equal to "http://localhost:9200/"
    // [
    //     'host' => 'localhost',    // Only host is required
    // ]
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
}

echo "Test GUI";

?>