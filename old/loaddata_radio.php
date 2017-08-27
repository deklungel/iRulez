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
                    
// create a new EditableGrid object
$grid = new EditableGrid();

require_once('language.php'); 

/* 
*  Add columns. The first argument of addColumn is the name of the field in the databse. 
*  The second argument is the label that will be displayed in the header
*/
$grid->addColumn('id', 'ID', 'integer', NULL, false); 
$grid->addColumn('naam', ucfirst($language['radio_grid1']), 'string');  
$grid->addColumn('omschrijving', ucfirst($language['radio_grid2']), 'string');  
$grid->addColumn('space_id', ucfirst($language['radio_grid3']), 'string', fetch_pairs($mysqli,'SELECT html_space.id, concat(html_verdiep.naam," - ",name) as space FROM html_space Join html_verdiep on html_verdiep = html_verdiep.id ORDER by html_verdiep.id ASC'),true);  
$grid->addColumn('favoriet', ucfirst($language['radio_grid4']), 'boolean');

$mydb_tablename = (isset($_GET['db_tablename'])) ? stripslashes($_GET['db_tablename']) : 'html_vButton';
                                                                       
$result = $mysqli->query('SELECT * FROM '.$mydb_tablename);
$mysqli->close();

// send data to the browser
$grid->renderJSON($result);

