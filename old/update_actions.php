<?php
//Version 2.5

foreach ($_POST as $key => $value) {
  echo $key."-->";
  echo var_dump($value);
	echo "</br>";
}
$fail = false;

$vButton_ID = $_POST['VbuttonID'];

if (isset($_POST['Update'])){
	update();
	updatOldDB($vButton_ID);
	if($fail == false){	
		mysqli_close($mysqli);
		header("Location: edit.php?table=vButton_actions&reload");
		exit;
	}
}
if (isset($_POST['add_action'])){
	add_action($_POST['add_action']);
	update();
	if($fail == false){	
		mysqli_close($mysqli);
		header("Location: edit.php?table=wizard&id=".$vButton_ID);
		exit;
	}
	
}
if (isset($_POST['del_action'])){
	del_action($_POST['del_action']);
	update();
	if($fail == false){	
		mysqli_close($mysqli);
		header("Location: edit.php?table=wizard&id=".$vButton_ID);
		exit;
	}
}
if (isset($_POST['add_arduino'])){
	add_arduino($_POST['add_arduino']);
	update();
	if($fail == false){	
		mysqli_close($mysqli);
		header("Location: edit.php?table=wizard&id=".$vButton_ID);
		exit;
	}
}
if (isset($_POST['del_arduino'])){
	del_arduino($_POST['del_arduino']);
	update();
	if($fail == false){	
		mysqli_close($mysqli);
		header("Location: edit.php?table=wizard&id=".$vButton_ID);
		exit;
	}
}
if (isset($_POST['del_kodi'])){
	del_kodi($_POST['del_kodi']);
	update();
	if($fail == false){	
		mysqli_close($mysqli);
		header("Location: edit.php?table=wizard&id=".$vButton_ID);
		exit;
	}
}
if (isset($_POST['add_kodi'])){
	add_kodi($_POST['add_kodi']);
	update();
	if($fail == false){	
		mysqli_close($mysqli);
		header("Location: edit.php?table=wizard&id=".$vButton_ID);
		exit;
	}
}
if (isset($_POST['Cancel'])){
		mysqli_close($mysqli);
		header("Location: edit.php?table=vButton_actions");
		exit;
}
if (isset($_POST['Update_Kodi'])){
		$result = get_actionID($vButton_ID);
		if($result == Null){
			add_action('K|1');
			$result = get_actionID($vButton_ID);
		}
		echo $result;
		
		if(isset($_POST['addKodi'])){
			echo "Test";
			updateKodi($result,$_POST['addKodi']);
		}
		else{
			del_action($result);
		}
		updatOldDB_Kodi($vButton_ID,$result);
		mysqli_close($mysqli);
		header("Location: edit.php?table=vButton_actions");
		exit;
}

function updateKodi($result,$addKodi){
	echo $result;
	echo var_dump($addKodi);
	del_all_kodi($result);
	add_all_kodi($result,$addKodi);
}

function update(){
	$VbuttonID = $_POST["VbuttonID"];
	$ActionType = $_POST["ActionType"];
	$MultipleActionSec = $_POST["MultipleActionSec"];
	$motionDetection = $_POST["motionDetection"];
	$motionDetectionIdle = $_POST["motionDetectionIdle"];
	$FBL = $_POST["FBL"];
	$FBLRelaisID = (isset($_POST["FBLRelaisID"]) ? $_POST["FBLRelaisID"] : "" );
	$delay = $_POST["delay"];
	
	if($ActionType != '3'){
		$MultipleActionSec = 0;
	}
	if($motionDetection == '0'){
		$motionDetectionIdle =0;
	}
	$sqlUpdate_Core_vButtonDB = "UPDATE Core_vButtonDB SET Mode=".$ActionType.", secBetweenActions=".$MultipleActionSec.", MD=".$motionDetection.", IdleTime=".$motionDetectionIdle.",FBL='".$FBL."',Delay=".$delay." WHERE id=".$VbuttonID;
	processSQL($sqlUpdate_Core_vButtonDB);
	$sqlDeleteFBL_from_Core_vButtonDB_actions_FBL = "DELETE FROM Core_vButtonDB_actions_FBL WHERE Core_vButtonDB_id =".$VbuttonID;
	processSQL($sqlDeleteFBL_from_Core_vButtonDB_actions_FBL);
	
	$sqlAddFBL_to_Core_vButtonDB_actions_FBL ="";
	
	if($FBL != '0'){
		$tmp ="";
		if($FBLRelaisID != ""){
			foreach ($FBLRelaisID as $value){
				$tmp = $tmp."(".$VbuttonID.",".$value."),";
			}
			
			$sqlAddFBL_to_Core_vButtonDB_actions_FBL = "INSERT INTO Core_vButtonDB_actions_FBL VALUES ".rtrim($tmp,',');
			processSQL($sqlAddFBL_to_Core_vButtonDB_actions_FBL);
		}
	}
	
	
	// echo $sqlUpdate_Core_vButtonDB."<br>";
	// echo $sqlDeleteFBL_from_Core_vButtonDB_actions_FBL."<br>";
	// echo $sqlAddFBL_to_Core_vButtonDB_actions_FBL."<br>";
	
	processActions("1");
	
	if($ActionType == '3'){
		if(processActions("2") == false && isset($_POST['add_action']) == false){
			$sqlUpdate_Core_vButtonDB = "UPDATE Core_vButtonDB SET Mode=0 WHERE id=".$VbuttonID;
			processSQL($sqlUpdate_Core_vButtonDB);
		}
	}
	else{
		$sqlDelete_2the_actions = "DELETE FROM Core_vButtonDB_actions WHERE action_nummer = 2 AND core_vButtonDB_id=".$VbuttonID;
		processSQL($sqlDelete_2the_actions);
		//echo $sqlDelete_2the_actions."</br>";
	}
	
		
	
	
	//execute sqlUpdate_Core_vButtonDB
	//execute sqlDeleteFBL_from_Core_vButtonDB_actions_FBL
	if($sqlAddFBL_to_Core_vButtonDB_actions_FBL != ""){
		//execute sqlAddFBL_to_Core_vButtonDB_actions_FBL
	}
}

function add_action($post){
	global $vButton_ID;
	$pieces = explode("|", $post);
	// echo $pieces[0]."</br>";
	// echo $pieces[1]."</br>";
	$sql = "INSERT INTO Core_vButtonDB_actions (core_vButtonDB_id, type, action_nummer) VALUES ('".$vButton_ID."','".$pieces[0]."', '".$pieces[1]."')";
	processSQL($sql);
	echo $sql;
}
function del_action($post){
	$sql = "DELETE FROM Core_vButtonDB_actions WHERE id = ".$post;
	processSQL($sql);
	echo $sql;
}
function get_actionID($tmp){
	global $mysqli;
	$sql = "SELECT id FROM Core_vButtonDB_actions WHERE core_vButtonDB_id = ".$tmp;
	$action = mysqli_query($mysqli,$sql);
	$row = mysqli_num_rows($action);
	// echo $row;
	if($row > 0){
		return mysqli_fetch_row($action)[0];
	}
	else{
		return Null;
	}

}
function add_arduino($post){
	if (isset($_POST['addArduino'.$post])){
		$arduino = $_POST['addArduino'.$post];
		$sql = "INSERT INTO Core_vButtonDB_actions_Arduino (Core_vButtonDB_actions_id, Core_Arduino_Outputs_id , Dimmer) VALUES ('".$post."', '".$arduino."', '0')";
		processSQL($sql);
		//echo $sql;
	}
}
function add_kodi($post){
	if (isset($_POST['addKodi'.$post])){
		$kodi = $_POST['addKodi'.$post];
		$sql = "INSERT INTO Core_vButtonDB_actions_Kodi (Core_vButtonDB_actions_id, html_Radio_id) VALUES ('".$post."', '".$kodi."')";
		processSQL($sql);
		//echo $sql;
	}
}
function add_all_kodi($Core_vButtonDB_actions_id,$html_Radio_id){
	foreach ($html_Radio_id as $value){
		$sql = "INSERT INTO Core_vButtonDB_actions_Kodi (Core_vButtonDB_actions_id, html_Radio_id) VALUES ('".$Core_vButtonDB_actions_id."', '".$value."')";
		processSQL($sql);
		echo $sql;
	}
}
function del_arduino($post){
	$pieces = explode("|", $post);
	// echo $pieces[0]."</br>";
	// echo $pieces[1]."</br>";
	$sql = "DELETE FROM Core_vButtonDB_actions_Arduino WHERE Core_vButtonDB_actions_id = '".$pieces[0]."' AND Core_Arduino_Outputs_id =".$pieces[1];
	processSQL($sql);
	//echo $sql;
}
function del_kodi($post){
	$pieces = explode("|", $post);
	// echo $pieces[0]."</br>";
	// echo $pieces[1]."</br>";
	$sql = "DELETE FROM Core_vButtonDB_actions_Kodi WHERE Core_vButtonDB_actions_id = '".$pieces[0]."' AND html_Radio_id =".$pieces[1];
	processSQL($sql);
	//echo $sql;
}
function del_all_kodi($Core_vButtonDB_actions_id){
	$sql = "DELETE FROM Core_vButtonDB_actions_Kodi WHERE Core_vButtonDB_actions_id = ".$Core_vButtonDB_actions_id;
	processSQL($sql);
	echo $sql;
}
function processSQL($sql){
	global $mysqli, $fail;
	// echo $sql;
	if($fail == false){
		if(mysqli_query($mysqli, $sql)){
			// echo " - success</br>";
		}
		else{
			echo $sql." - fail</br>";
			echo "Error updating record: " . mysqli_error($mysqli). "</br>";
			$fail = true;
		}
	}
}

function processActions($i){
	//loop throw the actions for first action
	$action_id = (isset($_POST["action_id".$i]) ? $_POST["action_id".$i] : "");
	if($action_id != "" && isset($_POST['del_action']) == false){
		foreach ($action_id as $value){
				// echo $value."</br>";
				$DimSpeed=(isset($_POST["DimSpeed".$i][$value]) ? $_POST["DimSpeed".$i][$value] : '');
				$LightValue=(isset($_POST["LightValue".$i][$value]) ? $_POST["LightValue".$i][$value] : '');
				$Condition=(isset($_POST["Condition".$i.$value]) ? $_POST["Condition".$i.$value] : '');
				$SD_Before =(isset($_POST["SD_Before".$i][$value]) ? $_POST["SD_Before".$i][$value] : '0');
				$SD_After =(isset($_POST["SD_After".$i][$value]) ? $_POST["SD_After".$i][$value] : '0');
				$con=(isset($_POST["con".$i.$value]) ? $_POST["con".$i.$value] : '');
				$timer=(isset($_POST["timer".$i][$value]) ? $_POST["timer".$i][$value] : '');
				$mail=(isset($_POST["mail".$i][$value]) ? $_POST["mail".$i][$value] : '');
				$delay=(isset($_POST["delay".$i][$value]) && $_POST["delay"] != "0" ? $_POST["delay".$i][$value] : '0');
				$TypeActionDimmer=(isset($_POST["TypeActionDimmer".$i][$value]) ? $_POST["TypeActionDimmer".$i][$value] : '');
				$KodiActie=(isset($_POST["KodiActie".$i][$value]) ? $_POST["KodiActie".$i][$value] : '');
				$Kodizender=(isset($_POST["Kodizender".$i][$value]) ? $_POST["Kodizender".$i][$value] : '');
				$KodiVolume=(isset($_POST["KodiVolume".$i][$value]) ? $_POST["KodiVolume".$i][$value] : '');
				if($KodiVolume == '*'){
					$KodiVolume = (isset($_POST["Kodi_volume".$i][$value]) ? $_POST["Kodi_volume".$i][$value] : '100');
				}
		
			// echo "</br>";
			// echo var_dump($DimSpeed)."</br>";
			// echo var_dump($LightValue)."</br>";
			// echo var_dump($Condition)."</br>";
			// echo var_dump($con)."</br>";
			// echo var_dump($timer)."</br>";
			// echo var_dump($mail)."</br>";
			// echo var_dump($delay)."</br>";
			// echo var_dump($TypeActionDimmer)."</br>";
			// echo "</br>";
			
			$sqlDelete_Conditions = "DELETE FROM Core_vButtonDB_actions_Conditions WHERE Core_vButtonDB_actions_id=".$value;
			processSQL($sqlDelete_Conditions);
			//echo $sqlDelete_Conditions."</br>";
			
			$sqlDelete_Conditions_Waypoint = "DELETE FROM Core_vButtonDB_actions_Condition_Waypoint WHERE  	Core_vButtonDB_actions=".$value;
			processSQL($sqlDelete_Conditions_Waypoint);
			//echo $sqlDelete_Conditions_Waypoint."</br>";
			
			
			$tmp ="";
			$tmp2 = "";
			$SD = "0";
			if($Condition != 'NONE' && !(empty($con))){
				foreach ($con as $value2){
					if($value2 == "SD"){
						$SD = "1";
					}
					elseif(substr($value2,0,2) == 'WP'){
						$pieces = explode("|", $value2);
						$tmp2 = $tmp2."(".$value.",".$pieces[1].",'".$pieces[2]."'),";
					}
					elseif(substr($value2,0,1) == '!'){
						$value2 = str_replace('!','',$value2);
						$tmp = $tmp."(".$value.",".$value2.",'OFF'),";
					}
					else{
						$tmp = $tmp."(".$value.",".$value2.",'ON'),";	
					}			
				}
				if($tmp != ""){
				$sqlto_Core_vButtonDB_actions_Conditions= "INSERT INTO Core_vButtonDB_actions_Conditions VALUES ".rtrim($tmp,',');
				processSQL($sqlto_Core_vButtonDB_actions_Conditions);
				//echo $sqlto_Core_vButtonDB_actions_Conditions."<br>";
				}
				if($tmp2 != ""){
				$sqlto_Core_vButtonDB_actions_Condition_Waypoint= "INSERT INTO Core_vButtonDB_actions_Condition_Waypoint VALUES ".rtrim($tmp2,',');
				processSQL($sqlto_Core_vButtonDB_actions_Condition_Waypoint);
				//echo $sqlto_Core_vButtonDB_actions_Condition_Waypoint."<br>";
				}
			}
			
			
			$sqlUpdate_actions = "UPDATE Core_vButtonDB_actions SET ".($DimSpeed != "" ? " dim_speed=".$DimSpeed."," : "" ).(!(empty($con)) ? " `condition`='".$Condition."'," : "`condition`='NONE'," ).($LightValue != "" ? " light_level=".$LightValue."," : "" ).($timer != "" ? " timer=".$timer."," : "" )."mail='".$mail."', SD='".$SD."', ".($SD == 1 ? " SD_Before='".$SD_Before."',SD_After='".$SD_After."'," : "SD_Before='0',SD_After='0'," )." delay=".$delay.",".(!(empty($KodiActie)) ? " kodi_action='".$KodiActie."'," : "kodi_action=NULL," ).(!(empty($Kodizender)) ? " kodi_zender='".$Kodizender."'," : "kodi_zender=NULL," ).(!(empty($KodiVolume)) ? " kodi_volume='".$KodiVolume."'" : "kodi_volume=NULL" )." WHERE id=".$value;
			processSQL($sqlUpdate_actions);
			//echo $sqlUpdate_actions."</br>";
			
			
			
			
		
			$arduino_id = (isset($_POST["arduino_id".$i.$value]) ? $_POST["arduino_id".$i.$value] : "");
			if($arduino_id != ""){
				foreach ($arduino_id as $value3){
					echo "Value3 ".$value3."</br>";
					$Master=(isset($_POST["master".$i.$value]) ? $_POST["master".$i.$value] : '');
					$Dimmer=(isset($_POST["TypeActionDimmer".$i.$value][$value3]) ? '1' : '0');
					// echo "Master ".$Master."</br>";
					// echo "Dimmer ".$Dimmer."</br>";
					
					$sqlUpdateArduino="UPDATE Core_vButtonDB_actions_Arduino SET ".($Master == $value3 ? 'Master=1,' : 'Master=0,')." Dimmer=".$Dimmer." WHERE Core_Arduino_Outputs_id=".$value3." AND Core_vButtonDB_actions_id=".$value;
					processSQL($sqlUpdateArduino);
					//echo $sqlUpdateArduino."</br>";
				}
			}
			
			
			
			
		
		}
		return true;
	}
	elseif($i == '2'){
		return false;
	}
}

function updatOldDB_Kodi($id,$Core_vButtonDB_actions_id){
	global $mysqli;
	$html_Radio_id = mysqli_query($mysqli,"SELECT html_Radio_id FROM Core_vButtonDB_actions_Kodi WHERE Core_vButtonDB_actions_id=".$Core_vButtonDB_actions_id);
	$action = '';
	if (mysqli_num_rows($html_Radio_id) > 0){
		$action = 'K';
	}
	while($row = mysqli_fetch_assoc($html_Radio_id)) {
		$action = $action.'|'.$row["html_Radio_id"];
	}
	
	$sql = "UPDATE Core_vButtonDB SET actie = '".$action."' WHERE id =".$id;
	echo $action;
	echo $sql;
	processSQL($sql);
}

function updatOldDB($id){
	global $mysqli;
	$vbutton = mysqli_query($mysqli,"SELECT * FROM Core_vButtonDB WHERE id=".$id);
	$result   = mysqli_fetch_row($vbutton);
	echo var_dump($result);
	$begin = $result[3];
	if($result[3] == "3"){
		$begin .="|".$result[4];
	}
	if($result[3] == "1" && $result[5] != "0"){
		$begin .= "|W|".$result[6];
	}
	
	if($result[7] != "NONE"){
		$FBLSQL = mysqli_query($mysqli,"SELECT pin, arduino FROM Core_vButtonDB_actions_FBL join Core_Arduino_Outputs ON Core_vButtonDB_actions_FBL.Core_Arduino_Outputs_id = Core_Arduino_Outputs.id WHERE core_vButtonDB_id =".$id);
		$arduino="";
		$pin="";
		while($row = mysqli_fetch_assoc($FBLSQL)) {
			$arduino .= $row['arduino'].";";
			$pin .= $row['pin'].";";
		}
		$fblRelais= "|".rtrim($arduino,';')."|".rtrim($pin,';');
		$begin .="|".$result[7].($fblRelais != "||" ? $fblRelais : "");
	}
	
	
	$ActionSQL = mysqli_query($mysqli,"SELECT * FROM Core_vButtonDB_actions WHERE core_vButtonDB_id = ".$id);
	if($ActionSQL){
	$boolGlobal = true;	
	if(mysqli_num_rows($ActionSQL) == 0){
		$boolGlobal = false;
	}
	$action1 = "";
	$action2 = "";
	
	while($row = mysqli_fetch_assoc($ActionSQL)) {
	
	
		$relaisSQLDimmer = mysqli_query($mysqli,"SELECT pin, arduino, Dimmer FROM Core_vButtonDB_actions_Arduino JOIN Core_Arduino_Outputs ON Core_vButtonDB_actions_Arduino.Core_Arduino_Outputs_id = Core_Arduino_Outputs.id  WHERE Core_vButtonDB_actions_id =".$row['id']." AND Dimmer = 1 ORDER BY Master DESC");
		$relaisSQL = mysqli_query($mysqli,"SELECT pin, arduino, Dimmer FROM Core_vButtonDB_actions_Arduino JOIN Core_Arduino_Outputs ON Core_vButtonDB_actions_Arduino.Core_Arduino_Outputs_id = Core_Arduino_Outputs.id  WHERE Core_vButtonDB_actions_id =".$row['id']." AND Dimmer = 0 ORDER BY Master DESC");
			
			$arduino="";
			$pin="";
			$action="";
			$bool = false;
			while($row2 = mysqli_fetch_assoc($relaisSQLDimmer)) {
				$arduino .= $row2['arduino'].";";
				$pin .= $row2['pin'].";";
			}
			if("|".rtrim($arduino,';')."|".rtrim($pin,';') != '||'){
				$action .= "|BD|".$row['light_level']."|".$row['dim_speed']."|".rtrim($arduino,';')."|".rtrim($pin,';');
				$bool = true;
			}
			
			$arduino="";
			$pin="";
			while($row2= mysqli_fetch_assoc($relaisSQL)) {
				$arduino .= $row2['arduino'].";";
				$pin .= $row2['pin'].";";
			}
			if($row['type'] != "K" and "|".rtrim($arduino,';')."|".rtrim($pin,';') != '||'){
				$action .= "|R|".rtrim($arduino,';')."|".rtrim($pin,';');
				$bool = true;
			}
			if($row['type'] == "K"){
				$bool = true;
			}
			
			if($bool == false)
			{
				//$boolGlobal = false;
				if($row['action_nummer'] == 1){
					$action1 .= "|".$action."|E";
				}
				else{
					$action2 .= "|".$action."|E";
				}
				continue;
			}
			
			if($row['type'] == "T"){
				$action .= "|T|";
			}
			else if($row['type'] == "K"){
				$KodiRadio = mysqli_query($mysqli,"SELECT html_Radio_id FROM Core_vButtonDB_actions_Kodi WHERE Core_vButtonDB_actions_id = ".$row['id']);
				$kodi = "";
				while($row2 = mysqli_fetch_assoc($KodiRadio)) {		
					$kodi .= $row2['html_Radio_id'].";";
				}
				$kodi_action = "";
				if($row['kodi_action'] != ""){
					$kodi_action = "|".$row['kodi_action']."|";
					if ($row['kodi_action'] == 'PL'){
						$kodi_action .= "|".$row['kodi_zender']."|";
					}
				}
				$kodi_volume ="";
				if($row['kodi_volume'] != ""){
					$kodi_volume = "|V|".$row['kodi_volume']."|";
				}
				
				$action .= "|K|".rtrim($kodi,';')."|".$kodi_action."|".$kodi_volume;
				
			}
			else if($row['type'] != "BD"){
				$action .= "|".ucfirst(strtolower($row['type']))."|".$row['timer']."|";
				
			}


			
			if($row['mail'] != "" ){
				$action .="|M|".$row['mail']."|";
			}
			
			if($row['condition'] != "NONE"){
				$ConSQL = mysqli_query($mysqli,"SELECT pin, arduino, ON_OFF FROM Core_vButtonDB_actions_Conditions JOIN Core_Arduino_Outputs ON Core_vButtonDB_actions_Conditions.Core_Arduino_Outputs_id = Core_Arduino_Outputs.id WHERE Core_vButtonDB_actions_id =".$row['id']);
				if($ConSQL){
					$arduino="";
					$pin="";
					while($row4 = mysqli_fetch_assoc($ConSQL)) {
						$arduino .= $row4['arduino'].";";
						if($row4['ON_OFF'] == "OFF"){
							$pin .= "!".$row4['pin'].";";
						}
						else{
							$pin .= $row4['pin'].";";
						}
						
					}
					$action .="|".$row['condition']."|";
					if("|".rtrim($arduino,';')."|".rtrim($pin,';')."|" != "|||"){
						$action .= "R|".rtrim($arduino,';')."|".rtrim($pin,';')."|";
					}
					if($row['SD']){
						$action .="|SD;".$row['SD_Before'].";".$row['SD_After']."|";
					}
				}
				$Con_WP_SQL = mysqli_query($mysqli,"SELECT OwnTracks_Waypoint,Soort FROM Core_vButtonDB_actions_Condition_Waypoint WHERE Core_vButtonDB_actions =".$row['id']);
				if($Con_WP_SQL){
					$OUT= "";
					$IN= "";
					while($row1 = mysqli_fetch_assoc($Con_WP_SQL)) {
						if($row1['Soort'] == 'OUT'){
							$OUT .= $row1['OwnTracks_Waypoint'].";";
						}
						else{
							$IN .= $row1['OwnTracks_Waypoint'].";";
						}
							
					}
					if($OUT != ""){
						$action .="|WPO|".rtrim($OUT,';')."|";
					}
					if($IN != ""){
						$action .="|WPI|".rtrim($IN,';')."|";
					}
				}
	
			}
		
			if($row['delay'] == "1"){
				$action .="|D|".$result[8]."|";
			}
			
			if($row['action_nummer'] == 1){
				$action1 .= "|".$action."|E";
			}
			else{
				$action2 .= "|".$action."|E";
			}
	}
	if($result[3] == "3"){
		$action = $action2."|BTF|".$action1;
	}
	else{
		$action = $action1;
	}
	$action = str_replace('||','|',$action);
	$begin = str_replace('||','|',$begin);
	echo "<br><br>".str_replace('||','|',$begin.$action)."<br>";
	//$sql = "UPDATE Core_VButtons SET actie = '".str_replace('||','|',$begin.$action)."' WHERE id =".$id;
	//processSQL($sql);
	$sql = "UPDATE Core_vButtonDB SET actie = '".preg_replace('/(\|E)+/','|E',str_replace('||','|',$begin.$action))."' WHERE id =".$id;
	echo $sql;
	if ($boolGlobal == false){
		$sql = "UPDATE Core_vButtonDB SET actie = '' WHERE id =".$id;
	}
	processSQL($sql);
}
else{
		$sql = "UPDATE Core_vButtonDB SET actie = '' WHERE id =".$id;
		processSQL($sql);
	}

}
?>