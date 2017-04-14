<?php
	error_reporting(-1);

	require_once 'vendor/autoload.php';
	require_once 'src/InstagramScraper.php';
	use InstagramScraper\Exception\InstagramException;
	use InstagramScraper\Instagram;

	$file = file_get_contents($argv[1]);
	$file_output = $argv[2];

	$file_array = explode("\n", $file);
	$instagram = new Instagram();

	foreach($file_array as $i)
	{
		$id = $i;
		try{
			$media = Instagram::getLocationById($id);
			$json_output = json_encode($media);
			file_put_contents($file_output, $json_output."\n", FILE_APPEND);
		}
	    catch (\Exception $ex) {
	    	print_r($ex);
		}			
	}
?>
