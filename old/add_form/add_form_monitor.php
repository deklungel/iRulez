<!--Version 1.0 -->
<?php 
$result_soort = mysqli_query($mysqli,"SELECT * FROM Device_Template");
	
	echo '<!-- simple form, used to add a new row -->
		<div id="addform">

            <div class="row">
                <input type="text" id="ip" name="ip" placeholder="'.ucfirst($language['ADD_Form_IP']).'" />
            </div>		
			<div class="row duo">
				<input type="text" id="Description" name="Description" placeholder="'.ucfirst($language['ADD_Form_Description']).'" />
				<input type="text" id="owntrack" name="owntrack" placeholder="'.ucfirst($language['ADD_Form_OwntrackID']).'" />
            </div>	
            <div class="row tright">
              <a id="addbutton" class="button green" ><i class="fa fa-save"></i> '.ucfirst($language['ADD_Form_Apply']).'</a>
              <a id="cancelbutton" class="button delete">'.ucfirst($language['ADD_Form_Cancel']).'</a>
            </div>
        </div>';
		
						
		?>
		