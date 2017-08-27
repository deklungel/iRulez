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

// Get all parameter provided by the javascript
$naam = $mysqli->real_escape_string(strip_tags($_POST['naam']));
$tablename = $mysqli->real_escape_string(strip_tags($_POST['tablename']));

$return=false;
if($naam !=''){
	if ( $stmt = $mysqli->prepare("INSERT INTO ".$tablename."  (naam) VALUES (?)")) {
		
		$stmt->bind_param("s",$naam);
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
		$error .= "Geen naam ingevuld\n";
	}
}
echo $return ? "ok" : $error;