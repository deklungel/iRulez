<?php
//Version 1.0
if (isset($_POST['Update'])){
	$TimerID = $_POST["TimerID"];
	$naam = $_POST["naam"];
	$checkEnabled = $_POST["checkEnabled"];
	$vButton = $_POST["vButton"];
	$random = $_POST["random"];
	
	$Days = array();
	
	for ($x = 0; $x <= count($TimerID)-1; $x++) {
		if (isset($_POST["Days".$x])){
		$Days[$x] = $_POST["Days".$x];
		}
		else{
		$Days[$x] = "";	
		}
		if (!isset($checkEnabled[$x])){
			$checkEnabled[$x] = "0";
		}
		if (!isset($random[$x])){
			$random[$x] = "0";
		}
	}
	
	$hour1 = $_POST["hour1"];
	$min1 = $_POST["min1"];
	$delay1 = $_POST["delay1"];
	$hour2 = $_POST["hour2"];
	$min2 = $_POST["min2"];
	$delay2 = $_POST["delay2"];

	$error = false;
	for ($x = 0; $x <= count($TimerID)-1; $x++) {
		if($hour1[$x] == "sunset" || $hour1[$x] == "sunrise")
		{
			$Time1 = $hour1[$x];
			if($delay1[$x] > 0){
				$delay1[$x] = str_replace("+", "", $delay1[$x]);
				$Time1 = $Time1.'+'.$delay1[$x];
			}
			elseif($delay1[$x] < 0){
				$delay1[$x] = str_replace("-", "", $delay1[$x]);
				$Time1 = $Time1.'-'.$delay1[$x];
			}	
		}
		else{
				$Time1 = $hour1[$x].":".$min1[$x];
		}
		
		if($random[$x] == 1){
			if($hour2[$x] == "sunset" || $hour2[$x] == "sunrise")
			{
				$Time2 = $hour2[$x];
				if($delay2[$x] > 0){
					$delay2[$x] = str_replace("+", "", $delay2[$x]);
					$Time2 = $Time2.'+'.$delay2[$x];
				}
				elseif($delay1[$x] < 0){
					$delay2[$x] = str_replace("-", "", $delay2[$x]);
					$Time2 = $Time2.'-'.$delay2[$x];
				}	
			}
			else{
				$Time2 = $hour2[$x].":".$min2[$x];
			}
		}
		else{
			$Time2 = "00:00";
		}
		
		$DayNumber = "";
		for ($z = 0; $z <= count($Days[$x]) -1; $z++) {
			$DayNumber .= $Days[$x][$z]."|";
		}
		$DayNumber = rtrim($DayNumber, "|");
		$sql = "UPDATE Timer_Actions SET Naam='".$naam[$x]."',Time='".$Time1."',Time2='".$Time2."',Random='".$random[$x]."',Timer_Day='".$DayNumber."',enabled='".$checkEnabled[$x]."',Core_vButton_id='".$vButton[$x]."'  WHERE id=".$TimerID[$x];
		if (!mysqli_query($mysqli, $sql)) {
			echo "Error updating record: " . mysqli_error($mysqli);
			$error = true;
		}
	}
	mysqli_close($mysqli);	
	
	if(!$error){
		header("Location: edit.php?table=timer&reload");
	}
	
}
elseif(isset($_POST['Delete'])){
		$sql = "DELETE FROM Timer_Actions WHERE id=".$_POST['Delete'];
		if (!mysqli_query($mysqli, $sql)) {
			echo $sql."</br>";
			echo "Error updating record: " . mysqli_error($mysqli);
			
		}
		else{
			mysqli_close($mysqli);
			header("Location: edit.php?table=timer&reload");
		}
		mysqli_close($mysqli);
	}
elseif(isset($_POST['New'])){
		$sql = "INSERT INTO Timer_Actions (Naam, Time,Random,Core_vButton_id,enabled) VALUES ('New', '00:00','0', '0', '0');";
		if (!mysqli_query($mysqli, $sql)) {
			echo $sql."</br>";
			echo "Error updating record: " . mysqli_error($mysqli);
			
		}
		else{
			mysqli_close($mysqli);
			header("Location: edit.php?table=timer");
		}
		mysqli_close($mysqli);
	}
else
{
	header("Location: edit.php?table=timer");
	exit;
}