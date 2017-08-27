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
$id = $mysqli->real_escape_string(strip_tags($_POST['id']));
$tablename = $mysqli->real_escape_string(strip_tags($_POST['tablename']));

// This very generic. So this script can be used to update several tables.
$return=false;
$result = mysqli_query($mysqli,"SELECT * FROM ".$tablename." WHERE id='".$id."'");
$row = mysqli_fetch_assoc($result);

if ( $stmt = $mysqli->prepare("DELETE FROM ".$tablename."  WHERE id = ?")) {
	$stmt->bind_param("i", $id);
	$return = $stmt->execute();
	$stmt->close();
	
	if ($row['soort'] == "fa-list-ul"){
		unlink('radio/playlist/'.$row['naam'].'.m3u');
	}
}             
$mysqli->close();        

echo $return ? "ok" : "error";

      

