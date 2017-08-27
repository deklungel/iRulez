<?php
//Version 1.0	
$result = mysqli_query($mysqli,"SELECT * FROM html_Radio_zender_Soort WHERE Glyphicon NOT LIKE 'fa-list-ul'");
			echo '<!-- simple form, used to add a new row -->
			<div id="addform">

            <div class="row">
                <input type="text" id="naam" name="naam" placeholder="'.ucfirst($language['ADD_Form_Name']).'" />
            </div>
			<div class="row">
                <input type="text" id="url" name="url" placeholder="'.ucfirst($language['ADD_Form_URL']).'" />
            </div>
			<div class="row">
				 <select name="soort" id="soort" class="placeholder">
						<option selected disabled value=\'\'>'.ucfirst($language['ADD_Form_Type']).'</option>';
						
						if (mysqli_num_rows($result) > 0) {
							// output data of each row
							while($row = mysqli_fetch_assoc($result)) {
								echo "<option value='".$row['Glyphicon']."'>".$row['Naam']."</option>";
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