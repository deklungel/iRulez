<?php
//Version 1
?>

<div id="wrap">
<?php 
if (isset($_GET["id"]) && $_GET["id"]!=""){
	
$vButtonSQL = mysqli_query($mysqli,"SELECT Arduino_Type,pin,naam,omschrijving,Mode,secBetweenActions,MD,FBL,IdleTime,Delay,Core_vButtonDB.id as id FROM Core_vButtonDB INNER JOIN Core_Devices on Core_vButtonDB.Core_Devices = Core_Devices.id WHERE Core_vButtonDB.id =".$_GET ["id"]);
if($vButtonSQL){
	$vButton = mysqli_fetch_assoc($vButtonSQL);	
}	
if( $vButton["Arduino_Type"] != 2 || $vButton["pin"] != 7){
	echo '<form action="?table=update" method="post">';
	echo "<input type='hidden' name='VbuttonID' value='".$_GET ["id"]."'>";
	echo "<h1>Button Setup - ".$vButton['naam']."</h1>";
	echo ($vButton['omschrijving'] != "" ? "<h2>".$vButton['omschrijving']."</h2>" : "" );
	echo "</br>";

	echo "<h2>".ucfirst($language['wizard_btn_mode'])." <div class='tooltip'><i class='fa fa-info-circle' aria-hidden='true'></i><span class='tooltiptext'>".ucfirst($language['wizard_tool_1'])."</span></div></h2>";
	$ModeSQL = mysqli_query($mysqli,"SELECT * FROM Core_vButtonDB_Mode");
	if($ModeSQL){
		while($row = mysqli_fetch_assoc($ModeSQL)) {
			echo "<input type='radio' name='ActionType' value='".$row['code']."'".($vButton['Mode']==$row['code'] ? 'checked' : '')." onclick=\"show('".$row['display']."');hide('".$row['hide']."')\">".ucfirst($language[$row['omschrijving']]);
		}
	}
	echo "<p class='MultipleActions'".($vButton['Mode']!=3 ? ' style="display: none;"' : '').">Seconds between actions <input type='text' name='MultipleActionSec' value='".$vButton['secBetweenActions']."'></p>";


	echo "<div class='motion' ".($vButton['Mode']==1 ? '' : 'style="display: none;"').">";
	echo "<h2>".ucfirst($language['wizard_btn_motion'])." <div class='tooltip'><i class='fa fa-info-circle' aria-hidden='true'></i><span class='tooltiptext'>".ucfirst($language['wizard_tool_2'])."</span></div></h2>";
	echo "<input type='radio' name='motionDetection' value='0'".($vButton['MD']==0 ? 'checked' : '')." onclick=\"hide('idleTimer')\">".ucfirst($language['no']);
	echo "<input type='radio' name='motionDetection' value='1'".($vButton['MD']==1 ? 'checked' : '')." onclick=\"show('idleTimer')\">".ucfirst($language['yes']);
	echo "<p class='idleTimer' ".($vButton['MD'] != 1 ? 'style="display: none;"' : '').">Idle timer in miliseconds <input type='text' name='motionDetectionIdle' value='".($vButton['IdleTime'] !=null ? $vButton['IdleTime'] : '1800')."'></p>";
	echo "</div>";


	// Feedback light

	echo "<h2>".ucfirst($language['wizard_btn_fbl'])." <div class='tooltip'><i class='fa fa-info-circle' aria-hidden='true'></i><span class='tooltiptext'>".ucfirst($language['wizard_tool_3'])."</span></div></h2>";
	echo "<table>";
	$FBLSQL = mysqli_query($mysqli,"SELECT * FROM Core_vButtonDB_FBL WHERE code != 'NONE' ORDER BY volgorde");
	echo "<tr><td><input type='radio' name='FBL' value='NONE' ".($vButton['FBL'] == "NONE" ? 'checked' : '')." onclick=\"hide('fbl_relais')\">".ucfirst($language['FBL_Mode_3'])."</td>";
	echo "<td rowspan='".($FBLSQL->num_rows+1)."'>";
	echo "<p class='fbl_relais' ".($vButton['FBL'] == "NONE" ? 'style="display: none;"' : '').">";
	$Arduino_Outputs_first = mysqli_query($mysqli,"SELECT Core_Arduino_Outputs.id, Core_Arduino_Outputs.naam, Core_vButtonDB_actions_FBL.Core_Arduino_Outputs_id as relais FROM Core_Arduino_Outputs LEFT OUTER JOIN Core_vButtonDB_actions_FBL  ON Core_vButtonDB_actions_FBL.Core_Arduino_Outputs_id = Core_Arduino_Outputs.id AND Core_vButtonDB_actions_FBL.Core_vButtonDB_id = ".$vButton['id']." ORDER BY Core_Arduino_Outputs.id");
	echo "<select name='FBLRelaisID[]' multiple>";
	echo "	<option disabled value='0' onclick=\"resetDropDown('FBLRelaisID[]')\">".ucfirst($language['FBL_Mode_3'])."</option>";
	if($Arduino_Outputs_first){
		while($row = mysqli_fetch_assoc($Arduino_Outputs_first)) {
			echo "<option value='".$row['id']."'".($row['relais'] != null ? ' selected ' : '').">".$row['naam']."</option>";
		}
	}
	echo "</select>";
	echo "</p></td></tr>";
	while($row = mysqli_fetch_assoc($FBLSQL)) {
		echo "<tr><td><input type='radio' name='FBL' value='".$row['code']."'".($vButton['FBL']==$row['code'] ? 'checked' : '')." onclick=\"show('fbl_relais')\">".ucfirst($language[$row['omschrijving']])."</td></tr>";
	}
	echo "</table>";


	//delay
	echo "<h2>".ucfirst($language['wizard_btn_delay'])." <div class='tooltip'><i class='fa fa-info-circle' aria-hidden='true'></i><span class='tooltiptext'>".ucfirst($language['wizard_tool_4'])."</span></div></h2>";
	echo "<input size='2' type='number' name='delay' min='0' value='".$vButton['Delay']."'>";



	echo "<h1>".ucfirst($language['wiz_relais'])."</h1>";

	for($i = 1; $i<=2; $i++){
		//Relais
		$Arduino_Type = mysqli_query($mysqli,"SELECT * FROM Core_vButtonDB_actions_type WHERE action <= ".$i." ORDER BY volgorde");
		$Arduino_Type_arr = [];
		while($row = mysqli_fetch_assoc($Arduino_Type)) {
			$Arduino_Type_arr[$row['code']] = array($row['omschrijving'],$row['enable'],$row['disable'],$row['hide'],$row['show'],$row['checkEnableDisable']);
		}
		if($i == 1){
			echo "<h2>".ucfirst($language['wiz_first'])."</h2>";
			echo "<button type='submit' class='btn btn-add' type='submit' name='add_action' value='T|".$i."'><i class='fa fa-plus-circle'></i> ".ucfirst($language['wiz_Toggle'])."</button> ";
			echo "<button type='submit' class='btn btn-add' type='submit' name='add_action' value='ON|".$i."'><i class='fa fa-plus-circle'></i> ".ucfirst($language['wiz_ON'])."</button> ";
			echo "<button type='submit' class='btn btn-add' type='submit' name='add_action' value='OFF|".$i."'><i class='fa fa-plus-circle'></i> ".ucfirst($language['wiz_OFF'])."</button> ";
			echo "<button type='submit' class='btn btn-add' type='submit' name='add_action' value='K|".$i."'><i class='fa fa-plus-circle'></i> ".ucfirst($language['wiz_Kodi'])."</button> ";
			echo "<div class='outputs'>";
		}
		else{
			echo "<div class='SecondAction'".($vButton['Mode']!=3 ? ' style="display: none;"' : '')."><h2>".ucfirst($language['wiz_second'])."</h2>";
			echo "<button type='submit' class='btn btn-add' type='submit' name='add_action' value='T|".$i."'><i class='fa fa-plus-circle'></i> ".ucfirst($language['wiz_Toggle'])."</button> ";
			echo "<button type='submit' class='btn btn-add' type='submit' name='add_action' value='ON|".$i."'><i class='fa fa-plus-circle'></i> ".ucfirst($language['wiz_ON'])."</button> ";
			echo "<button type='submit' class='btn btn-add' type='submit' name='add_action' value='OFF|".$i."'><i class='fa fa-plus-circle'></i> ".ucfirst($language['wiz_OFF'])."</button> ";
			echo "<button type='submit' class='btn btn-add' type='submit' name='add_action' value='BD|".$i."'><i class='fa fa-plus-circle'></i> ".ucfirst($language['wiz_Dimmer'])."</button> ";
			echo "<button type='submit' class='btn btn-add' type='submit' name='add_action' value='K|".$i."'><i class='fa fa-plus-circle'></i> ".ucfirst($language['wiz_Kodi'])."</button> ";
		}
		$ActionsSQL = mysqli_query($mysqli,"SELECT id, Core_vButtonDB_id, SD_Before, SD_After, Core_vButtonDB_actions_type.omschrijving, Type, dim_speed, Core_vButtonDB_actions.condition, light_level, timer, mail, action_nummer,SD, delay, kodi_action, kodi_zender, kodi_volume FROM Core_vButtonDB_actions inner join Core_vButtonDB_actions_type ON Core_vButtonDB_actions_type.code = Type WHERE Core_vButtonDB_id = ".$vButton['id']." AND action_nummer = ".$i);
		$idCounter = 0;
		while($row = mysqli_fetch_assoc($ActionsSQL)) {
			if($row['Type'] != 'K'){
				$sqlDimmer = mysqli_query($mysqli, "SELECT count(*) FROM Core_Arduino_Outputs INNER JOIN Core_vButtonDB_actions_Arduino ON Core_Arduino_Outputs.id = Core_vButtonDB_actions_Arduino.Core_Arduino_Outputs_id WHERE Core_vButtonDB_actions_id IN (SELECT id FROM Core_vButtonDB_actions WHERE Core_vButtonDB_actions_id = ".$row['id'].") AND Core_Arduino_Outputs_id IN (SELECT id FROM Core_Arduino_Outputs WHERE pin < 10)");
				$result   = mysqli_fetch_row($sqlDimmer);
				$sqlDimmerEnable = mysqli_query($mysqli, "SELECT count(*) FROM Core_Arduino_Outputs INNER JOIN Core_vButtonDB_actions_Arduino ON Core_Arduino_Outputs.id = Core_vButtonDB_actions_Arduino.Core_Arduino_Outputs_id WHERE Core_vButtonDB_actions_id IN (SELECT id FROM Core_vButtonDB_actions WHERE Core_vButtonDB_actions_id = ".$row['id'].") AND Core_vButtonDB_actions_Arduino.Dimmer = 1");
				$resultDimmerEnable   = mysqli_fetch_row($sqlDimmerEnable);
				$sundown = false;
				echo "<div id='borderAction'>";
				echo "<h3>".ucfirst($language[$row['omschrijving']])." <button type='submit' name='del_action' value='".$row['id']."'><i class='fa fa-trash-o red'></i></button></h3>";
				echo "<input type='hidden' name='action_id".$i."[]' value='".$row['id']."'>";
				echo "<table class='edite'>";
						echo "<tr>";
							echo ($result[0] > 0 ? '<th>'.ucfirst($language['wiz_Dim_setting']).'</th>' : '')."<th>".ucfirst($language['wiz_Cond_setting'])." <div class='tooltip'><i class='fa fa-info-circle' aria-hidden='true'></i><span class='tooltiptext'>".ucfirst($language['wizard_tool_7'])."</span></div></th>".($row['Type'] != 'T' ? "<th>".ucfirst($language['wiz_time_setting']). "<div class='tooltip'><i class='fa fa-info-circle' aria-hidden='true'></i><span class='tooltiptext'>".ucfirst($language['wizard_tool_8'])."</th>" : '')."<th>".ucfirst($language['wiz_email_setting']). " <div class='tooltip'><i class='fa fa-info-circle' aria-hidden='true'></i><span class='tooltiptext'>".ucfirst($language['wizard_tool_9'])."</th><th>".ucfirst($language['wiz_delay_setting'])." <div class='tooltip'><i class='fa fa-info-circle' aria-hidden='true'></i><span class='tooltiptext'>".ucfirst($language['wizard_tool_10'])."</span></div></th>";
					echo "</tr>";
					echo "<tr>";
						if($result[0] > 0){
						echo "<td>";
								echo '<table>';
									echo '<tr class="nobackground border_bottom">';
										echo '<td class="border">';
											echo ucfirst($language['wiz_Dim_SP_setting'])." <div class='tooltip'><i class='fa fa-info-circle' aria-hidden='true'></i><span class='tooltiptext'>".ucfirst($language['wizard_tool_5'])."</span></div>";
										echo '</td>';
										echo '<td class="border">';
											echo "<input ".($resultDimmerEnable[0] == 0 && $row['Type'] != "BD" ? " disabled " : "" )." type='number' id='DimSpeed".$i."[".$row['id']."]' name='DimSpeed".$i."[".$row['id']."]' value='".($row['dim_speed'] != null ? $row['dim_speed'] : '1000')."' min='1000' max='5000'>";
										echo '</td>';
									echo '</tr>';
	
									echo '<tr class="nobackground">';
										echo '<td class="border">';
											echo ucfirst($language['wiz_Dim_LL_setting'])." <div class='tooltip'><i class='fa fa-info-circle' aria-hidden='true'></i><span class='tooltiptext'>".ucfirst($language['wizard_tool_6'])."</span></div>";
										echo '</td>';
										echo '<td>';
											echo "<input  ".($resultDimmerEnable[0] == 0 && $row['Type'] != "BD" ? " disabled " : "" )."  type='number' id='LightValue".$i."[".$row['id']."]' name='LightValue".$i."[".$row['id']."]' value='".($row['light_level'] != null ? $row['light_level'] : '-1')."' min='-1' max='100'>";
										echo '</td>';
									echo '</tr>';
								echo '</table>';
						echo "</td>";
						}
						echo "<td>";
								echo "<table>";
								$Conditons = mysqli_query($mysqli,"SELECT * FROM Core_vButtonDB_actions_Condition ORDER by volgorde");
								echo "<tr class='nobackground'>";
									echo "<td>";
									while($row2 = mysqli_fetch_assoc($Conditons)) {
										$row2['enable'] = str_replace("$",$i.$row['id'],$row2['enable']);
										$row2['disable'] = str_replace("$",$i.$row['id'],$row2['disable']);
										$row2['hide'] = str_replace("*",$i.'['.$row['id'].']',$row2['hide']);
										echo "<input type='radio' ".($row2['code'] == $row['condition'] ? 'checked' : '')." name='Condition".$i.$row['id']."' value='".$row2['code']."'  onclick=\"enable('".$row2['enable']."');hide('".$row2['hide']."');disable('".$row2['disable']."');resetDropDown('".$row2['disable']."')\">".ucfirst($language[$row2['omschrijving']])."</br>"; 
									}
									echo "</td>";
									echo "<td class='center'>";
										$Arduino_Outputs_first = mysqli_query($mysqli,"SELECT Core_Arduino_Outputs.id, Core_Arduino_Outputs.naam, Core_vButtonDB_actions_Conditions.Core_Arduino_Outputs_id as vButton, Core_vButtonDB_actions_Conditions.ON_OFF FROM Core_Arduino_Outputs LEFT OUTER JOIN Core_vButtonDB_actions_Conditions  ON Core_vButtonDB_actions_Conditions.Core_Arduino_Outputs_id = Core_Arduino_Outputs.id AND Core_vButtonDB_actions_Conditions.Core_vButtonDB_actions_id = ".$row['id']." ORDER BY Core_Arduino_Outputs.id");
										$Waypoints = mysqli_query($mysqli,"SELECT OwnTracks_Waypoint.id, OwnTracks_Waypoint.Naam, Core_vButtonDB_actions_Condition_Waypoint.Soort, Core_vButtonDB_actions_Condition_Waypoint.Core_vButtonDB_actions as vButton FROM OwnTracks_Waypoint LEFT OUTER JOIN Core_vButtonDB_actions_Condition_Waypoint  ON Core_vButtonDB_actions_Condition_Waypoint.OwnTracks_Waypoint = OwnTracks_Waypoint.id AND Core_vButtonDB_actions_Condition_Waypoint.Core_vButtonDB_actions = ".$row['id']);
										echo "<select ".($row['condition'] == 'NONE' ? 'disabled' : '')." name='con".$i.$row['id']."[]' multiple>";
										echo "	<option ".($row['SD'] == "1" ? 'selected' : '' )." value='SD'  onclick=\"enable('SD_Before".$i."[".$row['id']."]|SD_After".$i."[".$row['id']."]');show('SD_Before".$i."[".$row['id']."]|SD_After".$i."[".$row['id']."]')\">".ucfirst($language['wiz_SunDown'])."</option>";
										if($row['SD'] == "1"){
											$sundown = true;
										}
										if($Waypoints){
											while($row3 = mysqli_fetch_assoc($Waypoints)) {
												echo "<option ".(($row3['vButton'] != null && $row3['Soort'] == 'OUT') ? 'selected' : '' )." value='WP|".$row3['id']."|OUT'>".$row3['Naam']." - ".ucfirst($language['wiz_OUT'])."</option>";
												echo "<option ".(($row3['vButton'] != null && $row3['Soort'] == 'IN') ? 'selected' : '' )." value='WP|".$row3['id']."|IN'>".$row3['Naam']." - ".ucfirst($language['wiz_IN'])."</option>";
											}
										}
										if($Arduino_Outputs_first){
											while($row3 = mysqli_fetch_assoc($Arduino_Outputs_first)) {
												echo "<option ".(($row3['vButton'] != null && $row3['ON_OFF'] != null && $row3['ON_OFF'] == 'ON') ? 'selected' : '' )." value='".$row3['id']."'>".$row3['naam']." - ".ucfirst($language['wiz_ON'])."</option>";
												echo "<option ".(($row3['vButton'] != null && $row3['ON_OFF'] != null && $row3['ON_OFF'] == 'OFF')? 'selected' : '' )." value='!".$row3['id']."'>".$row3['naam']."- ".ucfirst($language['wiz_OFF'])."</option>";
											}
										}
									
											echo "</select>";
									echo "</td>";
									echo "<td>";
										echo "<div class='SD_Before".$i."[".$row['id']."]' ".($row['SD'] == "0" ? 'style="display: none;"' : '').">".ucfirst($language['wiz_sdb_adj'])." <input size='5' type='text' ".($row['SD'] == "0" ? 'disabled' : '')." name='SD_Before".$i."[".$row['id']."]' value='".$row['SD_Before']."' ></div>";
										echo "<div class='SD_After".$i."[".$row['id']."]'  ".($row['SD'] == "0" ? 'style="display: none;"' : '').">".ucfirst($language['wiz_sda_adj'])." <input size='5' type='text' ".($row['SD'] == "0" ? 'disabled' : '')." name='SD_After".$i."[".$row['id']."]' value='".$row['SD_After']."'></div>";
									echo "</td>";
								echo "</tr>";
							echo "</table>";
						echo "</td>";
						
						if ($row['Type'] != 'T'){
						echo "<td class='center'>";
							echo "<input size='2' type='number' name='timer".$i."[".$row['id']."]' min='0' value='".($row['timer'] != null ? $row['timer'] : '0')."'></div>";
						echo "</td>";
						}
						echo "<td class='center'>";
								echo "<input size='25' type='email' name='mail".$i."[".$row['id']."]' value='".$row['mail']."'></div>";
						echo "</td>";
						echo "<td class='center'>";
								echo "<input type='checkbox' ".($row['delay'] == 1 ? 'checked' : '')." ' name='delay".$i."[".$row['id']."]' value='1'></div>";
						echo "</td>";
					echo "</tr>";	
				echo "</table>";
				echo "</br>";
				echo "<table class='edite'>";
				$ActionsArduino = mysqli_query($mysqli,"SELECT Core_Arduino_Outputs.naam,Core_Arduino_Outputs.omschrijving, Core_Arduino_Outputs.arduino, Core_vButtonDB_actions_Arduino.Dimmer,Core_vButtonDB_actions_Arduino.Core_Arduino_Outputs_id, Core_Arduino_Outputs.pin, Core_vButtonDB_actions_Arduino.Master FROM Core_Arduino_Outputs INNER JOIN Core_vButtonDB_actions_Arduino ON Core_Arduino_Outputs.id = Core_vButtonDB_actions_Arduino.Core_Arduino_Outputs_id WHERE Core_vButtonDB_actions_id =".$row['id']." ORDER BY Master DESC");
					echo "<tr>";
						echo "<th>".ucfirst($language['wiz_rel_naam'])."</th>".($row['Type'] == 'T'? "<th>".ucfirst($language['wiz_master'])."</th>" : "").($result[0] > 0 && $row['Type'] != "BD" ? '<th>'.ucfirst($language['wiz_Dimmer']).'</th>' : '')."<th>".ucfirst($language['wiz_delete'])."</th>";
						$collspan = 2;
						if($row['Type'] == 'T'){
							$collspan ++;
						}
						if ($result[0] > 0){
							$collspan ++;
						}
					echo "</tr>";
					$checkarr =[];
					while($row2 = mysqli_fetch_assoc($ActionsArduino)) {
					$checkarr[] = $row2['Core_Arduino_Outputs_id'];
					echo "<input type='hidden' name='arduino_id".$i.$row['id']."[]' value='".$row2['Core_Arduino_Outputs_id']."'>";
					echo "<tr>";
						echo "<td>";
							echo $row2['naam']." - ".$row2['omschrijving'];
						echo "</td>";
						if($row['Type'] == 'T'){
						echo "<td class='center'>";
							echo "<input type='radio' ".($row2['Master'] == 1 ? 'checked' : '')." name='master".$i.$row['id']."' value='".$row2['Core_Arduino_Outputs_id']."'>"; 
						echo "</td>";
						}
						if ($result[0] > 0){
							if($row['Type'] != "BD"){
								echo '<td class="center">';
									if($row2['pin'] < 10)
									{
									echo "<label class='TypeActionDimmer".$i.$row['id']."[".$idCounter."]'><input type='checkbox' ".($row2['Dimmer'] == 1 ? 'checked' : '')." name='TypeActionDimmer".$i.$row['id']."[".$row2['Core_Arduino_Outputs_id']."]' id='TypeActionDimmer".$i."[".$idCounter."]' value='1' onclick=\"enable('DimSpeed".$i."[".$row['id']."]|LightValue".$i."[".$row['id']."]')\"></label>";
									}
								echo '</td>';
							}
							else{
								echo "<input type='hidden' name='TypeActionDimmer".$i.$row['id']."[".$row2['Core_Arduino_Outputs_id']."]'' value='1'>";
							}
						}
						echo "<td class='center'>";
							echo "<button type='submit' name='del_arduino' value='".$row['id']."|".$row2['Core_Arduino_Outputs_id']."'><i class='fa fa-trash-o red'></i></button>";
						echo "</td>";
					echo "</tr>";
					}
					echo "<tr>";
						echo "<td class='center' colspan='".$collspan."'>";
							echo "<select name='addArduino".$row['id']."'>";
							if($row['Type'] != "BD"){
								$Arduino_Outputs = mysqli_query($mysqli,"SELECT id, naam, omschrijving FROM Core_Arduino_Outputs WHERE hidden = 0");
							}
							else{
								$Arduino_Outputs = mysqli_query($mysqli,"SELECT id, naam, omschrijving FROM Core_Arduino_Outputs WHERE pin < 10 AND hidden = 0");
							}
							if($Arduino_Outputs){
											while($row4 = mysqli_fetch_assoc($Arduino_Outputs)) {
												if (!in_array($row4['id'], $checkarr)) {
												echo "<option  value='".$row4['id']."'>".$row4['naam'].($row4['omschrijving'] != "" ? " - ".$row4['omschrijving'] : "" )."</option>";
												}
											}
							}
							echo "</select> ";
							echo "<button type='submit' class='btn btn-add' name='add_arduino' value='".$row['id']."'><i class='fa fa-plus-circle'></i> ".ucfirst($language['BTN_Add'])."</button> ";
						echo "</td>";
					echo "</tr>";
				echo "</table>";
				echo "</div>";
				
			$idCounter ++ ;
			}
			else{
				echo "<div id='borderAction'>";
					echo "<h3>".ucfirst($language[$row['omschrijving']])." <button type='submit' name='del_action' value='".$row['id']."'><i class='fa fa-trash-o red'></i></button></h3>";
					echo "<input type='hidden' name='action_id".$i."[]' value='".$row['id']."'>";
					echo "<table class='edite'>";
						echo "<tr>";
								echo "<th>".ucfirst($language['wiz_action'])."</th><th>".ucfirst($language['wiz_vol'])."</th>";
						echo "</tr>";
						echo "<tr>";
								echo "<td>";
									echo "<input type='radio' name='KodiActie".$i."[".$row['id']."]' value=''".($row['kodi_action']=="" ? ' checked ' : '')." onclick=\"disable('Kodizender".$i."[".$row['id']."]')\">None</br>";
									echo "<input type='radio' name='KodiActie".$i."[".$row['id']."]' value='PA'".($row['kodi_action']=="PA" ? ' checked ' : '')." onclick=\"disable('Kodizender".$i."[".$row['id']."]')\"><i class='fa fa-pause fa-3' aria-hidden='true'></i></br>";
									echo "<input type='radio' name='KodiActie".$i."[".$row['id']."]' value='PL'".($row['kodi_action']=="PL" ? ' checked ' : '')." onclick=\"enable('Kodizender".$i."[".$row['id']."]')\" ><i class='fa fa-play fa-3' aria-hidden='true'></i> ";
									
									$Zenderlijst_music = mysqli_query($mysqli,"SELECT id, naam FROM html_Radio_zenders WHERE soort = 'fa-music'");
									$Zenderlijst_youtube = mysqli_query($mysqli,"SELECT id, naam FROM html_Radio_zenders WHERE soort = 'fa-youtube'");
									$Zenderlijst_playlist = mysqli_query($mysqli,"SELECT id, naam FROM html_Radio_zenders WHERE soort = 'fa-list-ul'");
									echo "<select ".($row['kodi_action']!="PL" ? ' disabled ' : '')." name='Kodizender".$i."[".$row['id']."]'>";
									echo '<optgroup label="Radio">';
									while($row5 = mysqli_fetch_assoc($Zenderlijst_music)) {
											echo "<option  ".($row['kodi_zender'] == $row5['id']? " selected " : "" )." value='".$row5['id']."'>".$row5['naam']."</option>";
									}
									echo '<optgroup label="Youtube">';
									while($row5 = mysqli_fetch_assoc($Zenderlijst_youtube)) {
											echo "<option  ".($row['kodi_zender'] == $row5['id']? " selected " : "" )." value='".$row5['id']."'>".$row5['naam']."</option>";
									}
									echo '<optgroup label="Playlist">';
									while($row5 = mysqli_fetch_assoc($Zenderlijst_playlist)) {
											echo "<option  ".($row['kodi_zender'] == $row5['id']? " selected " : "" )." value='".$row5['id']."'>".$row5['naam']."</option>";
									}
									
									echo "</select> ";
									echo "</br>";
									echo "<input type='radio' name='KodiActie".$i."[".$row['id']."]' value='ST'".($row['kodi_action']=="ST" ? ' checked ' : '')." onclick=\"disable('Kodizender".$i."[".$row['id']."]')\"><i class='fa fa-stop fa-3' aria-hidden='true'></i></br>";
									echo "<input type='radio' name='KodiActie".$i."[".$row['id']."]' value='PT'".($row['kodi_action']=="PT" ? ' checked ' : '')." onclick=\"disable('Kodizender".$i."[".$row['id']."]')\" ><i class='fa fa-refresh fa-3' aria-hidden='true'></i> ";
								echo "</td>";
								echo "<td>";
									echo "<input type='radio' name='KodiVolume".$i."[".$row['id']."]' value=''".($row['kodi_volume']=="" ? ' checked ' : '').">".ucfirst($language['wiz_current'])."</i>";
									echo "</br>";
									echo "<input type='radio'  name='KodiVolume".$i."[".$row['id']."]' value='+'".($row['kodi_volume']=="+" ? ' checked ' : '')."><i class='fa fa-plus fa-3' aria-hidden='true'></i>";
									echo "</br>";
									echo "<input type='radio'  name='KodiVolume".$i."[".$row['id']."]' value='-'".($row['kodi_volume']=="-" ? ' checked ' : '')."><i class='fa fa-minus fa-3' aria-hidden='true'></i>";
									echo "</br>";
									echo "<input type='radio'  name='KodiVolume".$i."[".$row['id']."]' value='*'".($row['kodi_volume'] !="" && $row['kodi_volume'] !="+" && $row['kodi_volume'] !="-" ? ' checked ' : '')."><input type='number' min=0 max=100 name='Kodi_volume".$i."[".$row['id']."]'' value='".($row['kodi_volume'] !="" && $row['kodi_volume'] !="+" && $row['kodi_volume'] !="-" ? $row['kodi_volume'] : '0')."'><br></i>";
								echo "</td>";
						echo "</tr>";
						$ActionsKodi = mysqli_query($mysqli,"SELECT html_Radio.id, html_Radio.naam FROM html_Radio INNER JOIN Core_vButtonDB_actions_Kodi ON html_Radio.id = Core_vButtonDB_actions_Kodi.html_Radio_id WHERE Core_vButtonDB_actions_id = ".$row['id']);
						echo "<tr>";
							echo "<th>".ucfirst($language['wiz_Kodi'])."</th><th>".ucfirst($language['wiz_delete'])."</th>";
						echo "</tr>";
						while($row5 = mysqli_fetch_assoc($ActionsKodi)) {
						echo "<tr>";
							echo "<td>".$row5['naam'];
							echo "</td>";
							echo "<td class='center'>";
								echo "<button type='submit' name='del_kodi' value='".$row['id']."|".$row5['id']."'><i class='fa fa-trash-o red'></i></button>";
							echo "</td>";
						echo "</tr>";	
						}
					echo "</table>";
					echo "</br>";
					echo "<table class='edite'>";
						echo "<tr>";
						echo "<td class='center'>";
							echo "<select name='addKodi".$row['id']."'>";
							$Kodi = mysqli_query($mysqli,"SELECT id, naam FROM html_Radio");
							if($Kodi){
								while($row4 = mysqli_fetch_assoc($Kodi)) {
									echo "<option  value='".$row4['id']."'>".$row4['naam']."</option>";
								}
							}
							echo "</select> ";
							echo "<button type='submit' class='btn btn-add' name='add_kodi' value='".$row['id']."'><i class='fa fa-plus-circle'></i> ".ucfirst($language['BTN_Add'])."</button> ";
						echo "</td>";
					echo "</tr>";
					echo "</table>";
				echo "</div>";
			}
		}
			echo "</div>";
		
		
		}

		
	
echo "<br>";
echo "<div id='footer'>";
echo '<input type="submit" name="Cancel" value="'.ucfirst($language['BTN_cancel']).'"><input type="submit" name="Update" value="'.ucfirst($language['BTN_update']).'">';
echo "</div>";		
}
else{
	echo '<table>';
	echo "<tr>";
	echo "<td>";
	echo '<form action="?table=update" method="post">';	
	echo "<input type='hidden' name='VbuttonID' value='".$_GET ["id"]."'>";
			echo "<select multiple name='addKodi[]'>";
			$html_Radio = mysqli_query($mysqli,"SELECT id, naam FROM html_Radio");
			if($html_Radio){
				while($row4 = mysqli_fetch_assoc($html_Radio)) {
					$sql = "SELECT html_Radio_id FROM Core_vButtonDB_actions_Kodi WHERE html_Radio_id=".$row4['id']." and Core_vButtonDB_actions_id IN (SELECT id from Core_vButtonDB_actions where core_vButtonDB_id = ".$_GET ['id'].")";

					$check = mysqli_query($mysqli,$sql);	

					while ($tmp = mysqli_fetch_assoc($sql)){}
						if(mysqli_num_rows($check) > 0){
							echo "<option selected value='".$row4['id']."'>".$row4['naam']."</option>";
					 }
					else{
						echo "<option value='".$row4['id']."'>".$row4['naam']."</option>";
						$check = null;
					}
				}
			}
			echo "</select> ";
	echo "</td>";
	echo "</tr>";
	echo "<tr>";
	echo "<td>";
			echo "<a href='#' onclick='resetDropDown(\"addKodi[]\")'>".ucfirst($language['wiz_unselect'])."</a>";
	echo "</td>";
	echo "</tr>";
	echo '</table>';
	echo "<br>";
	echo "<div id='footer'>";
	echo '<input type="submit" name="Cancel" value="'.ucfirst($language['BTN_cancel']).'"><input type="submit" name="Update_Kodi" value="'.ucfirst($language['BTN_update']).'">';
	echo "</div>";
	echo "</form>";
	
}


} 
else{
	echo "No Id selected!";	
}
?>
<div>
<script src="js/wizard.js"></script>