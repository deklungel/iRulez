<?php
//Version 1.0	
$result_soort = mysqli_query($mysqli,"SELECT * FROM html_vButton_soort");
$result_space = mysqli_query($mysqli,"SELECT html_space.id as id, concat(html_verdiep.naam,' - ',name) as name FROM html_space Join html_verdiep on html_verdiep = html_verdiep.id ORDER by html_verdiep.id ASC");
$result_vButton = mysqli_query($mysqli,"SELECT * FROM Core_vButtonDB");
$result_glyphicon = mysqli_query($mysqli,"SELECT * FROM html_glyphicon");

			echo '<!-- simple form, used to add a new row -->
			<div id="addform">';
            echo '<div class="row">
                <input type="text" id="naam" name="naam" placeholder="'.ucfirst($language['ADD_Form_Name']).'" />
            </div>
			<div class="row duo">
				 <select name="space" id="space" class="placeholder">
						<option selected disabled value=\'\'>'.ucfirst($language['ADD_Form_Space']).'</option>';
						if (mysqli_num_rows($result_space) > 0) {
							// output data of each row
							while($row = mysqli_fetch_assoc($result_space)) {
								echo "<option value='".$row['id']."'>".$row['name']."</option>";
							}
						}
						
				echo '</select>
				<select name="soort" id="soort" class="placeholder">
						<option selected disabled value=\'\'>'.ucfirst($language['ADD_Form_Type']).'</option>';
					
						if (mysqli_num_rows($result_soort) > 0) {
							// output data of each row
							while($row = mysqli_fetch_assoc($result_soort)) {
								echo "<option value='".$row['id']."'>".ucfirst($language[$row['naam']])."</option>";
							}
						}

				echo'</select>
			</div>
			<div class="row trio">
				 <select name="vButton" id="vButton" class="placeholder">
						<option selected disabled value=\'\'>'.ucfirst($language['ADD_Form_vButton']).'</option>';
	
						if (mysqli_num_rows($result_vButton) > 0) {
							// output data of each row
							while($row = mysqli_fetch_assoc($result_vButton)) {
								echo "<option value='".$row['id']."'>".$row['naam']." - ".$row['omschrijving']."</option>";
							}
						}
				echo '</select>
				<select name="glyphicon" id="glyphicon" class="placeholder">
						<option selected disabled value=\'\'>'.ucfirst($language['ADD_Form_Glyphicon']).'</option>';

						if (mysqli_num_rows($result_glyphicon) > 0) {
							// output data of each row
							while($row = mysqli_fetch_assoc($result_glyphicon)) {
								echo "<option value='".$row['code']."'>".$row['naam']."</option>";
							}
						}
				echo '</select>
				<select id="favoriet" name="favoriet">
					  <option selected disabled value=\'0\'>'.ucfirst($language['ADD_Form_Favoriet']).'</option>
					  <option value="0">No</option>
					  <option value="1">Yes</option>
				</select>
			</div>			
            <div class="row tright">
              <a id="addbutton" class="button green" ><i class="fa fa-save"></i> '.ucfirst($language['ADD_Form_Apply']).'</a>
              <a id="cancelbutton" class="button delete"> '.ucfirst($language['ADD_Form_Cancel']).'</a>
            </div>
        </div>';
		?>