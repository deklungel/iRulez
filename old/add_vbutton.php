<?php
//Version 1.1
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
$space = $mysqli->real_escape_string(strip_tags($_POST['space']));
$soort = $mysqli->real_escape_string(strip_tags($_POST['soort']));
$glyphicon = $mysqli->real_escape_string(strip_tags($_POST['glyphicon']));
$vButton = $mysqli->real_escape_string(strip_tags($_POST['vButton']));
$favoriet = $mysqli->real_escape_string(strip_tags($_POST['favoriet']));
$tablename = $mysqli->real_escape_string(strip_tags($_POST['tablename']));

$return=false;
if($naam !='' and $space !='' and $soort !='' and $glyphicon !='' and $vButton !='' and $favoriet !=''){
	if ( $stmt = $mysqli->prepare("INSERT INTO ".$tablename."  (naam, glyphicon,favoriet,space_id,button_soort_id,vButton_id) VALUES (?,?,?,?,?,?)")) {
		$stmt->bind_param("ssiiii",$naam,$glyphicon,$favoriet,$space,$soort,$vButton);
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
	if ($space =='')
	{
		$error .= ucfirst($language['Error_Space'])."\n";
	}
	if ($soort =='')
	{
		$error .= ucfirst($language['Error_Type'])."\n";
	}
	if ($glyphicon =='')
	{
		$error .= ucfirst($language['Error_Glyphicon'])."\n";
	}
	if ($vButton =='')
	{
		$error .= ucfirst($language['Error_vButton'])."\n";
	}	
	if ($favoriet =='')
	{
		$error .= ucfirst($language['Error_favoriet'])."\n";
	}	
}
echo $return ? "ok" : $error;