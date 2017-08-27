<?php
//Version 1.0
/*
 * 
 * http://editablegrid.net
 *
 * Copyright (c) 2011 Webismymind SPRL
 * Dual licensed under the MIT or GPL Version 2 licenses.
 * http://editablegrid.net/license
 */
      
require_once('config.php');         

// Database connection                                   
$mysqli = mysqli_init();
$mysqli->options(MYSQLI_OPT_CONNECT_TIMEOUT, 5);
$mysqli->real_connect($config['db_host'],$config['db_user'],$config['db_password'],$config['db_name']); 

require_once('language.php'); 

// Get all parameter provided by the javascript
$naam = $mysqli->real_escape_string(strip_tags($_POST['naam']));
$url = $mysqli->real_escape_string(strip_tags($_POST['url']));
$soort = $mysqli->real_escape_string(strip_tags($_POST['soort']));
$tablename = $mysqli->real_escape_string(strip_tags($_POST['tablename']));

$return=false;
if($naam !='' and $soort !='' and $url !=''){
	if ( $stmt = $mysqli->prepare("INSERT INTO ".$tablename."  (naam, url,soort) VALUES (?,?,?)")) {
		
		$stmt->bind_param("sss",$naam,$url,$soort);
		$return = $stmt->execute();
		$stmt->close();
		$error = "error";
		$error= "INSERT INTO ".$tablename."  (naam, url,soort) VALUES (".$naam.",".$url.",".$soort.")";
	}             
	$mysqli->close();        
}
else{
	$error = "";
	if ($naam =='')
	{
		$error .= ucfirst($language['Error_Naam'])."\n";
	}
	if ($url =='')
	{
			$error .= ucfirst($language['Error_URL'])."\n";
	}
	if ($soort =='')
	{
			$error .= ucfirst($language['Error_Type'])."\n";
	}
}
echo $return ? "ok" : $error;