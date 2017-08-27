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

// echo ucfirst($language['vButton_grid1']);

// Database connection
$mysqli = mysqli_init();
$mysqli->options(MYSQLI_OPT_CONNECT_TIMEOUT, 5);
$mysqli->real_connect($config['db_host'],$config['db_user'],$config['db_password'],$config['db_name']); 

require_once('language.php'); 

function fetch_pairs_translation($mysqli,$query){
	global $language;
	if (!($res = $mysqli->query($query)))return FALSE;
	$rows = array();
	while ($row = $res->fetch_assoc()) {
		$first = true;
		$key = $value = null;
		foreach ($row as $val) {
			if ($first) { $key = $val; $first = false; }
			else { $value = $val; break; } 
		}
		$rows[$key] = ucfirst($language[$value]);
	}
	return $rows;
}


   
// create a new EditableGrid object
$grid = new EditableGrid();

/* 
*  Add columns. The first argument of addColumn is the name of the field in the databse. 
*  The second argument is the label that will be displayed in the header
*/
$grid->addColumn('id', 'ID', 'integer', NULL, false); 
$grid->addColumn('naam', ucfirst($language['vButton_grid1']), 'string');  
$grid->addColumn('space_id', ucfirst($language['vButton_grid2']), 'string', fetch_pairs($mysqli,'SELECT html_space.id, concat(html_verdiep.naam," - ",name) as space FROM html_space Join html_verdiep on html_verdiep = html_verdiep.id ORDER by html_verdiep.id ASC'),true);  
$grid->addColumn('button_soort_id', ucfirst($language['vButton_grid3']), 'string', fetch_pairs_translation($mysqli,'SELECT id, naam FROM html_vButton_soort'),true);
$grid->addColumn('glyphicon', ucfirst($language['vButton_grid4']), 'string' , fetch_pairs($mysqli,'SELECT code, naam FROM html_glyphicon'),true);  
$grid->addColumn('favoriet', ucfirst($language['vButton_grid5']), 'boolean');
$grid->addColumn('vButton_id', ucfirst($language['vButton_grid6']), 'string', fetch_pairs($mysqli,'SELECT id, naam FROM Core_vButtonDB'),true);
$grid->addColumn('volgorde', ucfirst($language['vButton_grid7']), 'integer', NULL, true); 
$grid->addColumn('action', ucfirst($language['vButton_grid8']), 'html', NULL, false, 'id'); 

$mydb_tablename = (isset($_GET['db_tablename'])) ? stripslashes($_GET['db_tablename']) : 'html_vButton';
                                                                       
$result = $mysqli->query('SELECT * FROM '.$mydb_tablename);
$mysqli->close();

// send data to the browser
$grid->renderJSON($result);

