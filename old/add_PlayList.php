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

$qry = $mysqli->query("SELECT Setting,value FROM Settings");
while($row = $qry->fetch_assoc()) {
	$config[$row["Setting"]] = $row["value"];
}

// Get all parameter provided by the javascript
$naam = $mysqli->real_escape_string(strip_tags($_POST['naam']));
$tablename = $mysqli->real_escape_string(strip_tags($_POST['tablename']));

$return=false;
if($naam !=''){
	if ( $stmt = $mysqli->prepare("INSERT INTO ".$tablename."  (naam,url,soort) VALUES (?,?,'fa-list-ul')")) {
		$url = $config['PlayListURL']."/".str_replace(' ','',$naam).".m3u";
		$stmt->bind_param("ss",$naam,$url);
		$return = $stmt->execute();
		$stmt->close();
		$error = "error";
	}             
	$mysqli->close();        
}
else{
	$error = "";
	if ($naam =='')
	{
		$error .= ucfirst($language['Error_Naam'])."\n";
	}
}
echo $return ? "ok" : $error;