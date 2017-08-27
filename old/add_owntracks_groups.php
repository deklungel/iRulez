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
$Monitor_Devices_id = $mysqli->real_escape_string(strip_tags($_POST['Monitor_Devices_id']));
$OwnTracks_Waypoint = $mysqli->real_escape_string(strip_tags($_POST['OwnTracks_Waypoint']));
$tablename = $mysqli->real_escape_string(strip_tags($_POST['tablename']));

require_once('language.php'); 

$return=false;

if($Monitor_Devices_id !='' && $OwnTracks_Waypoint !=''){
	if ( $stmt = $mysqli->prepare("INSERT INTO ".$tablename."  (Monitor_Devices_ID, waypoint_ID) VALUES (?,?)")) {
		$stmt->bind_param("ii",$Monitor_Devices_id,$OwnTracks_Waypoint);
		$return = $stmt->execute();
		$stmt->close();
		$error = "error";

	}             

	
	$mysqli->close();        
}
else{
	$error="";
	if($Monitor_Devices_id == ''){
	$error .= ucfirst($language['Error_Owntrack_Naam'])."\n";
	}
	if($OwnTracks_Waypoint == ''){
	$error .= ucfirst($language['Error_Waypoint'])."\n";
	}
}
echo $return ? "ok" : $error;