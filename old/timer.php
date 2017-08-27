<?php
//Version 1.0
?>
<div id="wrap">
<?php
echo '<form action="?table=update_Timer" method="post">';
echo "<table class='edite'>";
echo "<tr><th>".ucfirst($language['timer_grid1'])."</th><th>".ucfirst($language['timer_grid2'])."</th><th>".ucfirst($language['timer_grid3'])."</th><th>".ucfirst($language['timer_grid4'])."</th><th>".ucfirst($language['timer_grid5'])."</th><th>".ucfirst($language['timer_grid6'])."</th><th>".ucfirst($language['timer_grid7'])."</th><th>".ucfirst($language['timer_grid8'])."</th><tr>";
$Timers = mysqli_query($mysqli,"SELECT * FROM Timer_Actions");
$idCounter = 0;
while($Timer = mysqli_fetch_assoc($Timers)) {
	echo "<input type='hidden' name='TimerID[".$idCounter."]' value='".$Timer['id']."'>";
	echo "<tr>";
		echo "<td class='center'>";
			 echo "<input type='text' name='naam[".$idCounter."]' value='".$Timer['Naam']."'>";
		echo "</td>";
		echo "<td class='center'>";
			echo '<input type="checkbox" '; echo ($Timer['enabled']==1 ? "checked" : ""); echo ' name="checkEnabled['.$idCounter.']" value="1">';
		echo "</td>";
		echo "<td class='center'>";
			echo "<select name='vButton[".$idCounter."]'>";
					$vButtons = mysqli_query($mysqli,"SELECT * FROM Core_vButtonDB");
					while($vButton = mysqli_fetch_assoc($vButtons)) {
					echo "<option";
					if($vButton['id'] == $Timer['Core_vButton_id']){
						echo " selected";
					}
					echo " value='".$vButton['id']."'>".$vButton['naam']."</option>";
					}
			echo "</select>";
		echo "</td>";
		echo "<td class='center'>";
			echo "<select class='center' multiple name='Days".$idCounter."[]'>";
					$Days = mysqli_query($mysqli,"SELECT * FROM Timer_Day");
					while($Day = mysqli_fetch_assoc($Days)) {
					echo "<option";
					$explodeDays = explode("|", $Timer['Timer_Day']);
					foreach ($explodeDays as $explodeDay) {
					if($Day['id'] == $explodeDay){
						echo " selected";
					}
					}
					
					echo " value='".$Day['id']."'>".ucfirst($language[$Day['Name']])."</option>";
					}
			echo "</select>";
			echo "<a href='#' onclick='selectall(\"Days".$idCounter."[]\")'>".ucfirst($language['timer_select'])."</a> / <a href='#' onclick='unselectall(\"Days".$idCounter."[]\")'>".ucfirst($language['timer_unselect'])."</a>";
		echo "</td>";
		echo "<td class='center'>";
		
			if(strrpos($Timer['Time'], ":")){
				$time1 = explode(":", $Timer['Time']);
				$delay1[1] = "";
			}
			else{
				$time1[0]= $Timer['Time'];
				$time1[1]= "";
				$delay1[1] = "0";
				$delay1[0] = $Timer['Time'];
				if(strrpos($time1[0], "+")){
					$delay1 = explode("+", $time1[0]);
					$delay1[1] = "+".$delay1[1];
				}
				if(strrpos($time1[0], "-")){
					$delay1 = explode("-", $time1[0]);
					$delay1[1] = "-".$delay1[1];
				}	
			}
			echo "<p class ='hour1[".$idCounter."]' >";		
			echo "<select name='hour1[".$idCounter."]'>";
					
					echo "<option onclick='hide(\"min1[".$idCounter."]\");show(\"delay1[".$idCounter."]\")'";
					if($delay1[0] == "sunset"){
						echo " selected";
					}
					echo " value='sunset'>".ucfirst($language['timer_Sunset'])."</option>";
					echo "<option onclick='hide(\"min1[".$idCounter."]\");show(\"delay1[".$idCounter."]\")'";
					if($delay1[0] == "sunrise"){
						echo " selected";
					}
					echo " value='sunrise'>".ucfirst($language['timer_Sunrise'])."</option>";
					for ($x = 0;$x <= 23; $x++ ){
					echo "<option onclick='show(\"min1[".$idCounter."]\");hide(\"delay1[".$idCounter."]\")'";
					if((string)$x == (string)$time1[0]){
						echo " selected";
						
					}
					echo " value='".str_pad($x, 2, '0', STR_PAD_LEFT)."'>".str_pad($x, 2, '0', STR_PAD_LEFT)."</option>";
					}
			echo "</select>";
			echo "</p>";
			echo "<p class ='min1[".$idCounter."]' ";echo ($time1[1]== "" ? 'style="display:none"' : ''); echo ">";
			echo "<select name='min1[".$idCounter."]' >";
					for ($x = 0;$x <= 59; $x++ ){
					echo "<option ";
					if((string)$x == (string)$time1[1]){
						echo " selected";
						
					}
					echo " value='".str_pad($x, 2, '0', STR_PAD_LEFT)."'>".str_pad($x, 2, '0', STR_PAD_LEFT)."</option>";
					}
			echo "</select>";
			echo "</p>";
			echo "<p class='delay1[".$idCounter."]' ";echo (($delay1[1]== "" )  ? 'style="display:none"' : ''); echo ">";
			echo "<input type='text' name='delay1[".$idCounter."]' size='3' value='";echo (($delay1[1]== '' )  ? '0' : $delay1[1]); echo "'>";
			echo "</p>";
			echo "</td>";
			echo "<td class='center'>";
			echo " <input type='checkbox' name='random[".$idCounter."]' value='1'  onclick='OnChangeCheckbox(this,\"time2[".$idCounter."]\")'"; echo ($Timer['Random']== "1" ? 'checked' : ''); echo ">";
			echo "</td>";
			echo "<td class='center'>";
		
					if(strrpos($Timer['Time2'], ":")){
						$time2 = explode(":", $Timer['Time2']);
						$delay2[1]="";
					}
					else{
						$time2[0]= $Timer['Time2'];
						$time2[1]= "";
						$delay2[1] = "0";
						if(strrpos($time2[0], "+")){
							$delay2 = explode("+", $time2[0]);
						}
						if(strrpos($time2[0], "-")){
							$delay2 = explode("-", $time2[0]);
							$delay2[1] = "-".$delay2[1];
						}
					}
			echo "<div class='time2[".$idCounter."]' "; echo ($Timer['Random']== "1" ? '' : 'style="display:none"'); echo " >";	
				echo "<p class ='hour2[".$idCounter."]' >";
				echo "<select name='hour2[".$idCounter."]'>";
						echo "<option onclick='hide(\"min2[".$idCounter."]\");show(\"delay2[".$idCounter."]\")'";
						if($time2[0] == "sunset"){
							echo " selected";
						}
						echo " value='sunset'>".ucfirst($language['timer_Sunset'])."</option>";
						echo "<option onclick='hide(\"min2[".$idCounter."]\");show(\"delay2[".$idCounter."]\")'";
						if($time2[0] == "sunrise"){
							echo " selected";
						}
						echo " value='sunrise'>".ucfirst($language['timer_Sunrise'])."</option>";
						for ($x = 0;$x <= 23; $x++ ){
						echo "<option onclick='show(\"min2[".$idCounter."]\");hide(\"delay2[".$idCounter."]\")'";
						if((string)$x == (string)$time2[0]){
							echo " selected";
							
						}
						echo " value='".$x."'>".$x."</option>";
						}
				echo "</select>";
				echo "</p>";
					echo "<p class ='min2[".$idCounter."]'";echo (($time2[1]== "" )  ? 'style="display:none"' : ''); echo ">";
					echo "<select name='min2[".$idCounter."]'>";
							for ($x = 0;$x <= 59; $x++ ){
							echo "<option";
							if((string)$x == (string)$time2[1]){
								echo " selected";
								
							}
							echo " value='".$x."'>".$x."</option>";
							}
					echo "</select>";
				echo "</p>";
				echo "<p class='delay2[".$idCounter."]' ";echo (($delay2[1]== "" )  ? 'style="display:none"' : ''); echo ">";
					echo "<input type='text' name='delay2[".$idCounter."]' size='3' value='";echo (($delay2[1]== '' )  ? '0' : $delay2[1]); echo "'>";
				echo "</p>";
			echo "</div>";
		echo "</td>";
		echo "<td class='center'>";
			echo "<button class= 'button' type='submit' name='Delete' onclick=\"return confirm('Are you sure you want to delete timer ".$Timer['Naam']."?')\" value='".$Timer['id']."'><i class='fa fa-trash-o red fa-2x' ></i></button>";
		echo "</td>";
	echo "</tr>";
$idCounter++;
}
echo "</table>";
echo "<div class='submitcenter'>";
		echo '<button class="button green" type="submit" name="New"><i class="fa fa-plus"></i> '.ucfirst($language['timer_New']).'</button>';
		echo "<button class= 'button delete' type='submit' name='Update'><i class='fa  fa-arrow-circle-right'></i> ".ucfirst($language['timer_Save'])."</button>";
		echo '<a href="/edit.php?table=timer" class="button reset"><i class="fa fa-undo "></i> '.ucfirst($language['timer_Reset']).'</a>';
echo "</div>";
echo "</form>";
 
?>
</div>

<script src="js/timer.js"></script>