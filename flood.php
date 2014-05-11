<?php
/**************
* This is a simple script to communicate with a Fronius DataManager.
* It gets the realtime power being generated, and the total generated today.
* The values are appended to a simple CSV file - YYYY-MM-DD.csv
* The script can be run as often as desired.
* It will only query the inverter if the time is between sunrise and sunset.
* It will only record a value if the DataManager is able to communicate with the inverter.
* If the current time is after sunset, the script will draw a graph (if it does not already exist).
* The first time the graph is drawn, it is posted to Twitter.
* Copyright Terence Eden.  MIT Licence.
***************/

/*	Libraries to include	*/

//	Twitter Async from https://github.com/jmathai/twitter-async - no Licence specified
include 'lib/EpiTwitter/EpiCurl.php';
include 'lib/EpiTwitter/EpiOAuth.php';
include 'lib/EpiTwitter/EpiTwitter.php';

/*	Global variables	*/

//	Twitter OAuth tokens from https://dev.twitter.com/
//	Make sure app has read AND write permissions
$twitterConsumerKey    = "";
$twitterConsumerSecret = "";
$twitterToken          = "";
$twitterTokenSecret    = "";

//	Path of the script - to ensure we're reading and writing the correct directory
$currentPath = dirname(__FILE__) . DIRECTORY_SEPARATOR;

//	Calculate the timezone offset
$this_timezone = new DateTimeZone(date_default_timezone_get());
$now = new DateTime("now", $this_timezone);
$offset = $this_timezone->getOffset($now);


$forecastURL = "http://flooddata.alphagov.co.uk/3df.xml";

$xmlData = file_get_contents($forecastURL);


$floodData = simplexml_load_string($xmlData);

//print_r($floodData->day1image);

$day1image = base64_decode($floodData->day1image);
$day2image = base64_decode($floodData->day2image);
$day3image = base64_decode($floodData->day3image);

file_put_contents ( "day1image.png" , $day1image);
file_put_contents ( "day2image.png" , $day2image);
file_put_contents ( "day3image.png" , $day3image);

//	Post the image to Twitter
$twitterObj = new EpiTwitter($twitterConsumerKey, $twitterConsumerSecret, $twitterToken, $twitterTokenSecret);

$graph1Image = "$currentPath" . "$day1image";
$graph2Image = "$currentPath" . "$day2image";
$graph3Image = "$currentPath" . "$day3image";

$status1 = "Here is the flood warning map for today.";
$status2 = "Here is the flood warning map for tomorrow.";
$status3 = "Here is the flood warning map for the day after tomorrow.";

$uploadResp1 = $twitterObj->post('/statuses/update_with_media.json', 
                                array('@media[]' => "@{$graph1Image};type=png;filename={$day1image}",
                                'status' => $status1));

$uploadResp2 = $twitterObj->post('/statuses/update_with_media.json', 
                                array('@media[]' => "@{$graph2Image};type=png;filename={$day2image}",
                                'status' => $status2));

$uploadResp3 = $twitterObj->post('/statuses/update_with_media.json', 
                                array('@media[]' => "@{$graph3Image};type=png;filename={$day3image}",
                                'status' => $status3));


/*	All done, let's clean up after ourselves	*/
die();