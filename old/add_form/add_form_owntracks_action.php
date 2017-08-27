<?php
//Version 1.0	
$Monitor_Devices_id = mysqli_query($mysqli,"SELECT * FROM Monitor_Devices WHERE ownTracksID != ''");
$OwnTracks_Waypoint = mysqli_query($mysqli,"SELECT * FROM OwnTracks_Waypoint");
$Core_vButtonDB = mysqli_query($mysqli,"SELECT * FROM Core_vButtonDB");
$OwnTracks_event = mysqli_query($mysqli,"SELECT * FROM OwnTracks_event");

			echo '<!-- simple form, used to add a new row -->
			<div id="addform">

			<div class="row duo">
				 <select name="Monitor_Devices_id" id="Monitor_Devices_id" class="placeholder">
						<option selected disabled value=\'\'>'.ucfirst($language['ADD_Form_OwntrackID']).'</option>';
						
						if (mysqli_num_rows($Monitor_Devices_id) > 0) {
							// output data of each row
							while($row = mysqli_fetch_assoc($Monitor_Devices_id)) {
								echo "<option value='".$row['id']."'>".$row['ownTracksID']."</option>";
							}
						}
						
				echo '</select>
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
			<div class="row duo">
				 <select name="Core_vButtonDB" id="Core_vButtonDB" class="placeholder">
						<option selected disabled value=\'\'>'.ucfirst($language['ADD_Form_vButton']).'</option>';
	
						if (mysqli_num_rows($Core_vButtonDB) > 0) {
							// output data of each row
							while($row = mysqli_fetch_assoc($Core_vButtonDB)) {
								echo "<option value='".$row['id']."'>".$row['naam']."</option>";
							}
						}
				echo '</select>
				<select name="OwnTracks_event" id="OwnTracks_event" class="placeholder">
						<option selected disabled value=\'\'>'.ucfirst($language['ADD_Form_Event']).'</option>';

						if (mysqli_num_rows($OwnTracks_event) > 0) {
							// output data of each row
							while($row = mysqli_fetch_assoc($OwnTracks_event)) {
								echo "<option value='".$row['Naam']."'>".ucfirst($language[$row['Omschrijving']])."</option>";
							}
						}
				echo '</select>
			</div>			
            <div class="row tright">
              <a id="addbutton" class="button green" ><i class="fa fa-save"></i> '.ucfirst($language['ADD_Form_Apply']).'</a>
              <a id="cancelbutton" class="button delete">'.ucfirst($language['ADD_Form_Cancel']).'</a>
            </div>
        </div>';
		?>