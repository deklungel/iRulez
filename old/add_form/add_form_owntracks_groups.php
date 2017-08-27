<!--Version 1.0 -->
<?php 
$Monitor_Devices_id = mysqli_query($mysqli,"SELECT * FROM Monitor_Devices WHERE ownTracksID != ''");
$OwnTracks_Waypoint = mysqli_query($mysqli,"SELECT * FROM OwnTracks_Waypoint");
$result_soort = mysqli_query($mysqli,"SELECT * FROM Device_Template");
	
	echo '<!-- simple form, used to add a new row -->
		<div id="addform">	
			<div class="row">
				 <select name="Monitor_Devices_id" id="Monitor_Devices_id" class="placeholder">
						<option selected disabled value=\'\'>'.ucfirst($language['ADD_Form_OwntrackID']).'</option>';
						
						if (mysqli_num_rows($Monitor_Devices_id) > 0) {
							// output data of each row
							while($row = mysqli_fetch_assoc($Monitor_Devices_id)) {
								echo "<option value='".$row['id']."'>".$row['ownTracksID']."</option>";
							}
						}
						
				echo '</select>
				</div>
				<div class="row">
				<select name="OwnTracks_Waypoint" id="OwnTracks_Waypoint" class="placeholder">
						<option selected disabled value=\'\'>'.ucfirst($language['ADD_Form_Waypoint']).'</option>';
					
						if (mysqli_num_rows($OwnTracks_Waypoint) > 0) {
							// output data of each row
							while($row = mysqli_fetch_assoc($OwnTracks_Waypoint)) {
								echo "<option value='".$row['id']."'>".$row['Naam']."</option>";
							}
						}

				echo'</select>
			</div>
            <div class="row tright">
              <a id="addbutton" class="button green" ><i class="fa fa-save"></i> '.ucfirst($language['ADD_Form_Apply']).'</a>
              <a id="cancelbutton" class="button delete">'.ucfirst($language['ADD_Form_Cancel']).'</a>
            </div>
        </div>';
		
						
		?>
		