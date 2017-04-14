<?php
error_reporting(-1);

require_once 'vendor/autoload.php';
require_once 'src/InstagramScraper.php';
use InstagramScraper\Exception\InstagramException;
use InstagramScraper\Instagram;

$tag = $argv[1];
$maxid = $argv[2];
$file = "tag/".$tag."_result.txt";
$file2 = "tag/".$tag."_id.txt";

$instagram = new Instagram();
try {
	$result = Instagram::getPaginateMediasByTag($tag, $maxid);
	$medias = $result['medias'];
	$counter = 0;	
	foreach($medias as $i)
	{
		$fill = Instagram::getMediaById($i->id);
		$content = json_encode($fill)."\n";
		$counter++;
		file_put_contents($file, $content, FILE_APPEND);
	}
	
	$medias_status = true;
	while($result['hasNextPage'] == true && $counter <= 500000 && $medias_status = true) {
		$result = Instagram::getPaginateMediasByTag($tag, $result['maxId']);
		file_put_contents($file2, $result['maxId']."\n", FILE_APPEND);
		$medias = $result['medias'];
       		if($medias!= null) { $medias_status = true; }
		else { $medias_status = false; }
		foreach($medias as $i)
        	{
                	$fill = Instagram::getMediaById($i->id);
                	$content = json_encode($fill)."\n";
	                $counter++;
			file_put_contents($file, $content, FILE_APPEND);
	        }	
	}
} 

catch (\Exception $ex) {
	print_r($ex);
}
