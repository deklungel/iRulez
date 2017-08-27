<!--Version 1.0 -->
<?php 
$result_soort = mysqli_query($mysqli,"SELECT * FROM Device_Template");
	
	echo '<!-- simple form, used to add a new row -->
		<div id="addform">

            <div class="row">
                <input type="text" id="naam" name="naam" placeholder="'.ucfirst($language['ADD_Form_Name']).'" />
            </div>	
			<div class="row">
                <input type="text" id="description" name="description" placeholder="'.ucfirst($language['ADD_Form_Description']).'" />
            </div>				
            <div class="row tright">
              <a id="addbutton" class="button green" ><i class="fa fa-save"></i> '.ucfirst($language['ADD_Form_Apply']).'</a>
              <a id="cancelbutton" class="button delete">'.ucfirst($language['ADD_Form_Cancel']).'</a>
            </div>
        </div>';
		
						
		?>
		