<!--Version 1.0 -->
<?php 
$arduino = mysqli_query($mysqli,"SELECT COUNT(DISTINCT(arduino)) as totale FROM Core_VButtons ");
$count_arduino = mysqli_fetch_assoc($arduino);
$pinArray = [[]];

for ($i = 0; $i <= $count_arduino['totale']; $i++) {
		for ($j = 0; $j <= 15; $j++) {
			$pinArray[$i][$j] = 0;		
		}
}
for ($i = 0; $i <= $count_arduino['totale']; $i++) {
		$pin = mysqli_query($mysqli,"SELECT pin, arduino FROM Core_VButtons WHERE arduino = ".$i);
		if (mysqli_num_rows($pin) > 0) {
			// output data of each row
			while($row = mysqli_fetch_assoc($pin)) {
				$pinArray[$row['arduino']][$row['pin']] = 1;
			}
		}
}

			echo '<!-- simple form, used to add a new row -->
			<div id="addform">

            <div class="row">
                <input type="text" id="naam" name="naam" placeholder="Naam" />
            </div>		
			<div class="row">
                <input type="text" id="actie" name="actie" placeholder="Action" />
            </div>	
			<div class="row">
				 <select name="arduino" id="arduino" class="placeholder">
						<option selected disabled value="">Arduino</option>';
						for ($i = 0; $i <= $count_arduino['totale']; $i++) {
								for ($j = 0; $j <= 15; $j++) {
									if ($pinArray[$i][$j] == 0){
										echo "<option value='".$i."-".$j."'>Arduino ".$i." - Pin ".$j."</option>";
									}	
								}
						}	
						
						
			echo '</select>
            <div class="row tright">
              <a id="addbutton" class="button green" ><i class="fa fa-save"></i> Apply</a>
              <a id="cancelbutton" class="button delete">Cancel</a>
            </div>
        </div>';
		
						
		?>
		