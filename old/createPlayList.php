 <script src="js/jquery-2.2.3.min.js"></script>
  <script src="js/jquery-ui.js"></script>
<div id="wrap">
<script>
  $( function() {
	 var removeIntent = false;
	$( "#sortable2" ).sortable({
		revert: "invalid",
		update: function(event, ui) {
					 update();
				},
        
            over: function () {
                removeIntent = false;
            },
            out: function () {
                removeIntent = true;
            },
            beforeStop: function (event, ui) {
                if(removeIntent == true){
                    ui.item.remove();   
                }
            }
    });

	
    $( ".ui-state-default" ).draggable({
      connectToSortable: "#sortable2",
      helper: "clone",
      revert: "invalid"
    });
    $( "ul, li" ).disableSelection();
  } );
  
  function update(){
		var ids = $( "#sortable2" ).sortable('toArray', {attribute : 'data-id'});
		$('#list').val(ids);
		var titles = $( "#sortable2" ).sortable('toArray', {attribute : 'titles'});
		var titles2 = '';
		for (s of titles) {
			titles2  = titles2+'|'+s;
		}
		$('#list2').val(titles2.substr(1));
};

	function addlink(){
    var url = document.getElementById('url').value
	if(url.trim() != ""){
		var x = $("<li data-id='"+url+"' titles='"+url+"' class='ui-state-default'>"+url+"</li>");
		x.appendTo('#sortable2')
		$("#sortable2").sortable('refresh')
		update();
	}
	};
  </script>
  
 <h1><?php echo ucfirst($language['playlist_create1'])?></h1>
	<form action="?table=createPlaylist" method="post"> 
		<h2>MP3</h2>
		<ul id="sortable">
		  <?PHP
			$path = "radio/mp3/*";
				foreach (array_filter(glob($path), 'is_file') as $file)
				{
					echo '<li data-id="'.$file.'" titles="'.basename($file).'" class="ui-state-default">'.basename($file).'</li>';
				}
				
		?>
		</ul>
		<h2>Youtube</h2>
		<ul id="sortable">
		 <?PHP
			$sql_statement = "SELECT * FROM html_Radio_zenders where soort = 'fa-youtube'";
			$qry = $mysqli->query($sql_statement);
			while($row = $qry->fetch_assoc()) {
				echo '<li data-id="'.$row['url'].'"  titles="'.ucfirst($row['naam']).'" class="ui-state-default">'.ucfirst($row['naam']).'</li>';
			}
		 ?>
		</ul>
		
		<h2><?php echo ucfirst($language['playlist_create2'])?></h2>
		 <input id= 'url' type='text' name='url' value='' placeholder='Url'><button type="button" onclick="addlink()">Add</button>
		<ul id="sortable2">
			<?php
			$sql_statement = "SELECT * FROM html_Radio_playlist_Zender where html_Radio_playlist = '".$_GET['id']."'";
			$qry = $mysqli->query($sql_statement);
			while($row = $qry->fetch_assoc()) {
				echo '<li data-id="'.$row['url'].'" titles="'.ucfirst($row['Naam']).'" >'.ucfirst($row['Naam']).'</li>';
			}
			?>
		</ul>
		 
		<br style="clear:both">
 
		<input id="list" name="list"  type="hidden" value=''/>
		<input id="list2" name="list2"  type="hidden" value=''/>
		
		<?php
			$query = mysqli_query($mysqli,"SELECT * FROM html_Radio_zenders WHERE id = ".$_GET['id']);
			$playlist = mysqli_fetch_assoc($query);	
				echo "<input type='hidden' name='naam' value='".$playlist['naam']."' >";
				echo "<input type='hidden' name='url' value='".$playlist['url']."'>";
				echo "<input type='hidden' name='id' value='".$_GET['id']."'>";
		?>
		
		
		
		
		</br></br><button class= 'button green' type='submit' name='Create' onclick="update();"><i class='fa  fa-arrow-circle-right'></i> <?php echo ucfirst($language['playlist_create3'])?> </button>
	</form> 
</div>