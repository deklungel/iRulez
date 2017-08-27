<?php
//Version 1.0	
$result_event = mysqli_query($mysqli,"SELECT * FROM OwnTrack_event");
$result_vButton = mysqli_query($mysqli,"SELECT * FROM Core_vButtonDB");

			echo '<!-- simple form, used to add a new row -->
			<div id="addform">

            <div class="row">
                <input type="text" id="waypoint" name="waypoint" placeholder="Waypoint" />
            </div>
			<div class="row duo">
				  <select name="vButton" id="vButton" class="placeholder">
						<option selected disabled value=\'\'>vButton</option>';
	
						if (mysqli_num_rows($result_vButton) > 0) {
							// output data of each row
							while($row = mysqli_fetch_assoc($result_vButton)) {
								echo "<option value='".$row['id']."'>".$row['naam']."</option>";
							}
						}
				echo '</select>
				<select name="event" id="event" class="placeholder">
						<option selected disabled value=\'\'>Event</option>';
					
						if (mysqli_num_rows($result_event) > 0) {
							// output data of each row
							while($row = mysqli_fetch_assoc($result_event)) {
								echo "<option value='".$row['Naam']."'>".$row['Omschrijving']."</option>";
							}
						}

				echo'</select>
			</div>
            <div class="row tright">
              <a id="addbutton" class="button green" ><i class="fa fa-save"></i> Apply</a>
              <a id="cancelbutton" class="button delete">Cancel</a>
            </div>
        </div>';
		?>