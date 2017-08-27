<?php
//Version 1.0
$result_verdiep = mysqli_query($mysqli,"SELECT * FROM html_verdiep WHERE id != 0");

			echo '<!-- simple form, used to add a new row -->
			<div id="addform">

			<div class="row duo">
				<input type="text" id="naam" name="naam" placeholder="'.ucfirst($language['ADD_Form_Name']).'" />
				 <select name="verdiep" id="verdiep" class="placeholder">
						<option selected disabled value=\'\'>'.ucfirst($language['ADD_Form_Floor']).'</option>';
						
						if (mysqli_num_rows($result_verdiep) > 0) {
							// output data of each row
							while($row = mysqli_fetch_assoc($result_verdiep)) {
								echo "<option value='".$row['id']."'>".$row['naam']."</option>";
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