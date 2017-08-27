<!--Version 1.0 -->
<?php 
$result_soort = mysqli_query($mysqli,"SELECT * FROM Device_Template");
	
	echo '<!-- simple form, used to add a new row -->
		<div id="addform">

            <div class="row">
                <input type="text" id="mac" name="mac" placeholder="'.ucfirst($language['ADD_Form_MAC']).'" />
            </div>		
			<div class="row duo">
			<select name="soort" id="soort" class="placeholder">
						<option selected disabled value=\'\'>'.ucfirst($language['ADD_Form_Type']).'</option>';
					
						if (mysqli_num_rows($result_soort) > 0) {
							// output data of each row
							while($row = mysqli_fetch_assoc($result_soort)) {
								echo "<option value='".$row['id']."|".$row['Name']."'>".$row['Naam']."</option>";
							}
						}

				echo'</select>
				<input size="2" type="number" id="id" name="id" min="0" value ="0"/>
            </div>	
            <div class="row tright">
              <a id="addbutton" class="button green" ><i class="fa fa-save"></i> '.ucfirst($language['ADD_Form_Apply']).'</a>
              <a id="cancelbutton" class="button delete"> '.ucfirst($language['ADD_Form_Cancel']).'</a>
            </div>
        </div>';
		
						
		?>
		