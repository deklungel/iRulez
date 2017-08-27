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
        

// Database connection                                   
$mysqli = mysqli_init();
$mysqli->options(MYSQLI_OPT_CONNECT_TIMEOUT, 5);
$mysqli->real_connect($config['db_host'],$config['db_user'],$config['db_password'],$config['db_name']); 

// Get all parameter provided by the javascript
$ip = $mysqli->real_escape_string(strip_tags($_POST['ip']));
$Description = $mysqli->real_escape_string(strip_tags($_POST['Description']));
$owntrack = $mysqli->real_escape_string(strip_tags($_POST['owntrack']));
$tablename = $mysqli->real_escape_string(strip_tags($_POST['tablename']));

$return=false;
if($owntrack !=''){
	if ( $stmt = $mysqli->prepare("INSERT INTO ".$tablename."  (IP, Description, ownTracksID) VALUES (?,?,?)")) {
		$stmt->bind_param("sss",$ip,$Description,$owntrack);
		$return = $stmt->execute();
		$stmt->close();
		$mysqli->close(); 
		$error = "error";

	}     
}else{
	$error = ucfirst($language['Error_Owntrack'])."\n";
}
        

	

echo $return ? "ok" : $error;