<?php
//Version 1.0	
$result_verdiep = mysqli_query($mysqli,"SELECT * FROM html_verdiep WHERE id != 0");
			echo '<!-- simple form, used to add a new row -->
			<div id="addform">

            <div class="row">
                <input type="text" id="naam" name="naam" placeholder="Naam" />
            </div>
			<div class="row duo">
				 <select name="verdiep" id="verdiep" class="placeholder">
						<option selected disabled value=\'\'>Verdiep</option>';
						
						if (mysqli_num_rows($result_verdiep) > 0) {
							// output data of each row
							while($row = mysqli_fetch_assoc($result_verdiep)) {
								echo "<option value='".$row['id']."'>".$row['naam']."</option>";
							}
						}
						
				echo '</select>
			</div>
			<div class="row">
				<select id="favoriet" name="favoriet">
					  <option selected disabled value=\'0\'>Favoriet</option>
					  <option value="0">No</option>
					  <option value="1">Yes</option>
				</select>
			</div>			
            <div class="row tright">
              <a id="addbutton" class="button green" ><i class="fa fa-save"></i> Apply</a>
              <a id="cancelbutton" class="button delete">Cancel</a>
            </div>
        </div>';
		?>