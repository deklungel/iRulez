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
$MAC = $mysqli->real_escape_string(strip_tags($_POST['mac']));
$soort = $mysqli->real_escape_string(strip_tags($_POST['soort']));
$id = $mysqli->real_escape_string(strip_tags($_POST['id']));
$tablename = $mysqli->real_escape_string(strip_tags($_POST['tablename']));

if($soort == ''){
	$soort = '|';
}

$pieces = explode("|", $soort);
$soort = $pieces[0];
$Naam = $pieces[1].$id;

$return=false;
$return2=false;
$result = mysqli_query($mysqli,"SELECT * FROM ".$tablename." WHERE Nummer='".$Naam."'");
$row_cnt = mysqli_num_rows($result);

$result2 = mysqli_query($mysqli,"SELECT * FROM ".$tablename." WHERE MAC='".$MAC."'");
$row_cnt2 = mysqli_num_rows($result2);

if($row_cnt > 0 ){
	$error .= ucfirst($language['Error_Naam_uniek'])."\n";
	$return2=true;
}
if($row_cnt2 > 0 ){
	$error .= ucfirst($language['Error_Mac_uniek'])."\n";
	$return2=true;
}

if($MAC !='' && $Naam  !='' && $soort != '' && $return2==false){
	if ( $stmt = $mysqli->prepare("INSERT INTO ".$tablename."  (MAC, Nummer, Arduino_Type) VALUES (?,?,?)")) {
		$stmt->bind_param("ssi",$MAC,$Naam,$soort);
		$return = $stmt->execute();
		$stmt->close();
		$error = "error";
		$error = "INSERT INTO ".$tablename."  (MAC, Nummer, Arduino_Type) VALUES ('".$MAC."','".$Naam."',".$soort.")";

	}             
	if ($return){
		$result = mysqli_query($mysqli,"SELECT * FROM ".$tablename." WHERE MAC='".$MAC."'");
		$row = mysqli_fetch_assoc($result);
		if ($row['Arduino_Type'] !== "3") {
			$result2 = mysqli_query($mysqli,"SELECT * FROM Device_Template WHERE id='".$row['Arduino_Type']."'");
			$arduino = str_replace('Arduino','',$row['Nummer']);
			$row2 = mysqli_fetch_assoc($result2);
			for($i = 0; $i < $row2['Input'];$i++){
				$stmt = $mysqli->prepare("INSERT INTO Core_vButtonDB (naam,arduino,pin,actie,Core_Devices) VALUES ('".$row2['DefaultName'].$arduino."/".$i."','".$arduino."','".$i."','',".$row['id'].")");
				$return = $stmt->execute();
				$stmt->close();
			}
			if($row['Arduino_Type'] == "2"){
				for($i = 0; $i < $row2['Output'];$i++){
					if($i == 7){
						$stmt = $mysqli->prepare("INSERT INTO Core_Arduino_Outputs (naam,arduino,pin,hidden,Core_Devices_id) VALUES ('".$row2['DefaultName'].$arduino."/".$i."','".$arduino."','".$i."',1,".$row['id'].")");
					}
					else{
						$stmt = $mysqli->prepare("INSERT INTO Core_Arduino_Outputs (naam,arduino,pin,hidden,Core_Devices_id) VALUES ('".$row2['DefaultName'].$arduino."/".$i."','".$arduino."','".$i."',0,".$row['id'].")");
					}
					$return = $stmt->execute();
					$stmt->close();
				}
			}
			else{
				for($i = 0; $i < $row2['Output'];$i++){
					$stmt = $mysqli->prepare("INSERT INTO Core_Arduino_Outputs (naam,arduino,pin,hidden,Core_Devices_id) VALUES ('".$row2['DefaultName'].$arduino."/".$i."','".$arduino."','".$i."',0,".$row['id'].")");
					$return = $stmt->execute();
					$stmt->close();
				}
			}
			
		}
		else{
			$stmt = $mysqli->prepare("INSERT INTO html_Radio (id,naam,Core_Devices_id) VALUES (".str_replace("Kodi","",$row['Nummer']).",'".$row['Nummer']."',".$row['id'].")");
			$return = $stmt->execute();
			$stmt->close();
		}
		
		
	}
	
	$mysqli->close();        
}
elseif($return2 == false){
	$error = "";
	if ($Naam =='')
	{
		$error .= ucfirst($language['Error_Naam'])."\n";
	}
	if ($MAC =='')
	{
		$error .= ucfirst($language['Error_Mac'])."\n";
	}
	if ($soort =='')
	{
		$error .= ucfirst($language['Error_Type'])."\n";
	}
	$error = "TEST";
}
echo $return ? "ok" : $error;