<?php
//Version 1.0    


/*
 * examples/mysql/loaddata.php
 * 
 * This file is part of EditableGrid.
 * http://editablegrid.net
 *
 * Copyright (c) 2011 Webismymind SPRL
 * Dual licensed under the MIT or GPL Version 2 licenses.
 * http://editablegrid.net/license
 */
                              


/**
 * This script loads data from the database and returns it to the js
 *
 */
       
require_once('config.php');      
require_once('editableGrid.php');            

/**
 * fetch_pairs is a simple method that transforms a mysqli_result object in an array.
 * It will be used to generate possible values for some columns.
*/
function fetch_pairs($mysqli,$query){
	if (!($res = $mysqli->query($query)))return FALSE;
	$rows = array();
	while ($row = $res->fetch_assoc()) {
		$first = true;
		$key = $value = null;
		foreach ($row as $val) {
			if ($first) { $key = $val; $first = false; }
			else { $value = $val; break; } 
		}
		$rows[$key] = $value;
	}
	return $rows;
}


// Database connection
$mysqli = mysqli_init();
$mysqli->options(MYSQLI_OPT_CONNECT_TIMEOUT, 5);
$mysqli->real_connect($config['db_host'],$config['db_user'],$config['db_password'],$config['db_name']); 

require_once('language.php'); 

          
// create a new EditableGrid object
$grid = new EditableGrid();

/* 
*  Add columns. The first argument of addColumn is the name of the field in the databse. 
*  The second argument is the label that will be displayed in the header
*/
$grid->addColumn('id', 'ID', 'string', NULL, false); 
$grid->addColumn('MAC', ucfirst($language['devices_grid1']), 'string', NULL, true); 
$grid->addColumn('Nummer', ucfirst($language['devices_grid2']), 'string', NULL, true);  
$grid->addColumn('Arduino_Type', ucfirst($language['devices_grid3']), 'string' , fetch_pairs($mysqli,'SELECT id, Naam FROM Device_Template'),false);  
$grid->addColumn('Versie', ucfirst($language['devices_grid4']), 'string', 'string', Null ,false);
$grid->addColumn('IP', ucfirst($language['devices_grid5']), 'string', Null ,false);
$grid->addColumn('Type', ucfirst($language['devices_grid6']), 'string', Null ,false);
$grid->addColumn('Ping', ucfirst($language['devices_grid7']), 'string', Null ,false);
$grid->addColumn('MQTT', ucfirst($language['devices_grid8']), 'string', Null ,false);
$grid->addColumn('action', ucfirst($language['devices_grid9']), 'html', NULL, false, 'id'); 

$mydb_tablename = (isset($_GET['db_tablename'])) ? stripslashes($_GET['db_tablename']) : 'Core_Devices';
                                                                       
$result = $mysqli->query('SELECT * FROM '.$mydb_tablename);
$mysqli->close();

// send data to the browser
$grid->renderJSON($result);

