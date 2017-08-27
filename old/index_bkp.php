<?php
//Version 1.5
require_once('config.php'); 

$boolradio = false;
// Database connection
$mysqli = mysqli_init();
$mysqli->options(MYSQLI_OPT_CONNECT_TIMEOUT, 5);
$mysqli->real_connect($config['db_host'],$config['db_user'],$config['db_password'],$config['db_name']); 
    
$qry = $mysqli->query("SELECT Setting,value FROM Settings");
while($row = $qry->fetch_assoc()) {
	$config[$row["Setting"]] = $row["value"];
}


if(empty($_GET["page"]))
{
	$page="favorieten";
}
else{
	$page=$_GET["page"];
}



?>

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">
	<link rel="icon" type="image/png" href="favicon.ico" />
    <title>iRulez</title>

    <!-- Bootstrap core CSS -->

    <link href="css/bootstrap.min.css" rel="stylesheet">
	<link href="css/bootstrap_extended.css" rel="stylesheet">	
    <link href="css/jasny-bootstrap.min.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="css/navmenu.css" rel="stylesheet">
	<link rel="stylesheet" type="text/css" href="css/block.css" />
	<link rel="stylesheet" type="text/css" href="css/easy-responsive-tabs.css" />
	<link rel="stylesheet" href="css/font-awesome.min.css">
	<link href="css/jasny-bootstrap-custom.css" rel="stylesheet">
	<link href="css/roundslider.min.css" rel="stylesheet" />
	
	<script src="js/jquery-2.2.3.min.js"></script>

	
    <!-- Just for debugging purposes. Don't actually copy this line! -->
    <!--[if lt IE 9]><script src="../../docs-assets/js/ie8-responsive-file-warning.js"></script><![endif]-->

    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->
	
	
  </head>

  <body>
    <div class="navmenu navmenu-default navmenu-fixed-left offcanvas-sm" role="navigation">
      <a class="navmenu-brand visible-md visible-lg" href="#"><img src="images/iRulez_Logo_Small.png" alt='i' id="iRulez_Logo"><i>R</i>ulez</a>
      <ul class="nav navmenu-nav">
		
		<?php
		$qry = $mysqli->query("SELECT naam,id FROM html_verdiep");

		while($row = $qry->fetch_assoc()) {
			 if ( strtolower($row['naam']) == strtolower($page) )
			{
				$qry2 = $mysqli->query("SELECT name FROM html_space where html_verdiep = ".$row['id']);
				if($qry2->num_rows == 0){
				echo "<li class='active'><a href='?page=".$row['naam']."'>".$row['naam']."</a></li>";
				}
				else{
					echo '<li class="dropdown open">';
					echo  '<a href="?page='.$row['naam'].'" class="dropdown-toggle" data-toggle="dropdown">'.$row['naam'].' <b class="caret"></b></a>';
					echo'  <ul class="dropdown-menu navmenu-nav" role="menu">';
					while($row2 = $qry2->fetch_assoc()) {
						echo'	<li><a href="#">'.$row2['name'].'</a></li>';
					}
					echo'  </ul>';
					echo '</li>';
				}
				
				
			}
			else{
				$qry2 = $mysqli->query("SELECT name FROM html_space where html_verdiep = ".$row['id']);
				if($qry2->num_rows == 0){
				echo "<li><a href='?page=".$row['naam']."'>".$row['naam']."</a></li>";	
				}
				else{
					echo '<li class="dropdown">';
					echo  '<a href="?page='.$row['naam'].'" class="dropdown-toggle" data-toggle="dropdown">'.$row['naam'].' <b class="caret"></b></a>';
					echo'  <ul class="dropdown-menu navmenu-nav" role="menu">';
					while($row2 = $qry2->fetch_assoc()) {
						echo'	<li><a href="#">'.$row2['name'].'</a></li>';
					}
					echo'  </ul>';
					echo '</li>';
				}
			}
		} 

		?>
		 
      </ul>
	  <ul class="nav navmenu-nav bottom">
	  <li><a class="btn" href="edit.php">Edit</a></li>
	  </ul>
    </div>

    <div class="navbar navbar-default navbar-fixed-top hidden-md hidden-lg">
      <button type="button" class="navbar-toggle" data-toggle="offcanvas" data-target=".navmenu" data-canvas="body">
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <a class="navbar-brand" href="#"><img src="images/iRulez_Logo_Small.png" alt='i' id="iRulez_Logo"><i>R</i>ulez</a>
    </div>

    <div class="container">
      <div class="page-header">
        <h1><?php echo ucfirst($page) ?></h1>
		<div id="notConnected"><h1 >Connecting to MQTT</h1></div>
      </div>
     <div id="watermark"><img id="iRulez_watermark" src="images/iRulez_Logo.png" alt='i'></img></div>
	         <!--Horizontal Tab-->
        <div id="parentHorizontalTab">
            <ul class="resp-tabs-list hor_1">
			<?PHP	
			if (strtolower($page) != strtolower("favorieten"))
			{
				$sql_statement = "SELECT * FROM html_vButton_soort 
				WHERE id IN 
					(SELECT button_soort_id FROM html_vButton 
					WHERE button_soort_id IN 
						(SELECT button_soort_id FROM html_vButton WHERE verdiep_id = (SELECT id FROM html_verdiep WHERE naam = '".$page."'))) ORDER BY id";
				$sql_statement2 = "SELECT * FROM html_Radio WHERE verdiep_id = (SELECT id FROM html_verdiep WHERE naam = '".$page."') ORDER BY id";
				
			}
			else{
				$sql_statement = "SELECT * FROM html_vButton_soort 
				WHERE id IN 
					(SELECT button_soort_id FROM html_vButton 
					WHERE button_soort_id IN 
						(SELECT button_soort_id FROM html_vButton)
					AND favoriet = '1'
					)
				ORDER BY id";
				$sql_statement2 = "SELECT * FROM html_Radio WHERE favoriet = '1' ORDER BY id";
			}
			$qry = $mysqli->query($sql_statement);
			$qry2 = $mysqli->query($sql_statement2);
			
				while($row = $qry->fetch_assoc()) {
					echo ("<li>".ucfirst($row['naam'])."</li>");
				}
				if (mysqli_num_rows($qry2) != 0) {
					if (strtolower($page) != strtolower("favorieten"))
					{
						$sql_statement3= "SELECT * FROM `html_vButton` WHERE  button_soort_id = 4
																AND verdiep_id = (
																	SELECT 
																		id 
																	FROM 
																		html_verdiep 
																	WHERE 
																		naam = '".$page."'
																)";
					}
					else{
						$sql_statement3= "SELECT * FROM `html_vButton` WHERE favoriet = 1 AND button_soort_id = 4 ";
					}
					$qry3 = $mysqli->query($sql_statement3);
					if (mysqli_num_rows($qry3) == 0) {
						echo "<li>".ucfirst("Radio")."</li>";
					}
				}
			?>
            </ul>
            <div class="resp-tabs-container hor_1">
                
				<?PHP
				$qry = $mysqli->query($sql_statement);
				
				if (mysqli_num_rows($qry) == 0 && mysqli_num_rows($qry2) == 0) {
						echo "</div>";
						echo "</div>";	
						if (strtolower($page) != strtolower("favorieten"))
						{			
							echo 'Add Vbuttons here';
						}
						else{	
							echo 'Add favorites here';
						}
				}
				else{
				
				while($row = $qry->fetch_assoc()) {
					
					echo "<div>";
						echo "<div class='container-fluid'>";
							echo "<div class='row'>";
								if (strtolower($page) != strtolower("favorieten"))
								{
								$sql_statement_vButton = "	SELECT 
																html_vButton.id AS id, 
																html_vButton.naam AS naam,
																html_vButton.favoriet AS favoriet,
																html_glyphicon.code AS glyphicon_code, 
																Core_vButtonDB.id AS vButton_id,
																Core_vButtonDB.actie AS actie,
																Core_vButtonDB.arduino AS arduino,
																Core_vButtonDB.pin AS pin
															FROM 
																html_vButton 
																INNER JOIN html_glyphicon ON html_vButton.glyphicon = html_glyphicon.code 
																INNER JOIN Core_vButtonDB ON html_vButton.vButton_id = Core_vButtonDB.id 
															WHERE 
																button_soort_id = '".$row['id']."' 
																AND verdiep_id = (
																	SELECT 
																		id 
																	FROM 
																		html_verdiep 
																	WHERE 
																		naam = '".$page."'
																)";
																
								}
								else
								{
								$sql_statement_vButton = "	SELECT html_vButton.id AS id, 
																html_vButton.naam AS naam, 
																html_glyphicon.code AS glyphicon_code,
																Core_vButtonDB.id AS vButton_id,
																Core_vButtonDB.actie AS actie,
																Core_vButtonDB.arduino AS arduino,
																Core_vButtonDB.pin AS pin
															FROM 
																html_vButton 
																INNER JOIN html_glyphicon ON html_vButton.glyphicon = html_glyphicon.code
																INNER JOIN Core_vButtonDB ON html_vButton.vButton_id = Core_vButtonDB.id
															WHERE button_soort_id = '".$row['id']."'
															AND favoriet = '1'";
				
								}
								$qry_vButton = $mysqli->query($sql_statement_vButton);

								$unique=0;
								while($vButton = $qry_vButton->fetch_assoc()) {
									$unique++;
									// echo "<button class='box image-block col-md-3 col-sm-3 col-xs-4 col-xxs-6 col-xxxs-6 col-xxxxs-12' onClick=doToggel('".$vButton['arduino'].'-'.$vButton['pin']."')>";
									// echo "<p class='content'>".$vButton['naam']."</br>";
									// echo "<i id='".$vButton['arduino'].'-'.$vButton['pin']."' class='fa ".$vButton['glyphicon_code']." fa-4'></i>";
									// echo "<p hidden class='id'>".$vButton['arduino']."-".$vButton['pin']."</p>";
									// echo "</p>";
									// echo "</button>";
									$pieces = explode("|", $vButton['actie']);
									
									if($pieces[0] == '3'  && ($pieces[2] == "BD" || $pieces[3] == "BD" || $pieces[5] == "BD")){
										$counter = 0;
										if ($pieces[3] == "BD"){
											$counter = 1;
										}
										if ($pieces[5] == "BD"){
											$counter = 3;
										}
											$piecesArduino = explode(";", $pieces[$counter + 5]);
											$piecesPin = explode(";", $pieces[$counter + 6]);
										
										//for ($x = 0; $x <= count($piecesArduino)-1; $x++) {
										
										echo "<div class='box image-block col-md-3 col-sm-3 col-xs-4 col-xxs-6 col-xxxs-6 col-xxxxs-12'>";
												echo "<div class='contentDimmer'>".$vButton['naam'];"</br>";
													echo '<div id="'.$unique.'vButton-'.$vButton['id'].'-Dimmer-'.$piecesArduino[0]."-".$piecesPin[0].'"></div>';
												echo "</div>";
												echo "<p hidden class='dimmerId'>".$piecesArduino[0]."-".$piecesPin[0]."</p>";
												echo "<p hidden class='id'>".$vButton['arduino']."-".$vButton['pin']."</p>";
										echo "</div>";
										
										echo' <script type="text/javascript">';
										echo' $(document).ready(function () {';
										echo'		$("#'.$unique.'vButton-'.$vButton['id'].'-Dimmer-'.$piecesArduino[0]."-".$piecesPin[0].'").roundSlider({';
										echo'			value: 0,';
										echo'			sliderType: "min-range",';
										echo'			handleShape: "square",';
										echo'			circleShape: "pie",';
										echo'			editableTooltip: false,';
										//echo'			width: "16",';
										echo'			min: "0",';
										echo'			step: "5",';
										echo'			max: "100",';
										//echo'			radius: 80,';
										echo'			startAngle: 315,';
										echo'			tooltipFormat: "changeTooltip'.$unique.'vButton'.$vButton['id'].'Dimmer'.$piecesArduino[0].$piecesPin[0].'",';
										echo'			drag: function(event) {';
										echo'				var value = event.value;';
										echo'				doDimmer(value,"';
															for ($x = 0; $x <= count($piecesArduino)-1; $x++) {
										echo 				$piecesArduino[$x].";";
															}
										echo				"|";
															for ($x = 0; $x <= count($piecesArduino)-1; $x++) {
										echo 				$piecesPin[$x].";";
															}
										echo 				'","'.$unique.'")';
										echo'			},';
										echo'			change: function(event) {';
										echo'				var value = event.value;';
										echo'				doDimmer(value,"';
															for ($x = 0; $x <= count($piecesArduino)-1; $x++) {
										echo 				$piecesArduino[$x].";";
															}
										echo				"|";
															for ($x = 0; $x <= count($piecesArduino)-1; $x++) {
										echo 				$piecesPin[$x].";";
															}
										echo 				'","'.$unique.'")';
										echo'			}';
										echo'		});';
										
										echo'	});';
										echo' </script>';
										
										echo' <script>';
										echo'			function changeTooltip'.$unique.'vButton'.$vButton['id'].'Dimmer'.$piecesArduino[0].$piecesPin[0].'(e) {';
										echo'			  	var val = e.value, speed;';
										echo"				if (typeof vButtonArray['".$vButton['arduino'].$vButton["pin"]."'] != 'undefined' && vButtonArray['".$vButton['arduino'].$vButton["pin"]."'] =='H'){";
										echo'					return val + "<div onclick=\"doToggel(\''.$vButton['arduino']."-".$vButton["pin"]."\',\'".$unique.'\')\"><i id=\"'.$vButton['arduino'].'-'.$vButton["pin"].'\" class=\'fa '.$vButton["glyphicon_code"].' fa-3x active\'></i></div>";';
										echo'				}';
										echo'				else{';
										echo'					return val + "<div onclick=\"doToggel(\''.$vButton['arduino']."-".$vButton["pin"]."'\,'".$unique.'\')\"><i id=\"'.$vButton['arduino'].'-'.$vButton["pin"].'\" class=\'fa '.$vButton["glyphicon_code"].' fa-3x\'></i></div>";';
										echo'				}';
										echo'			}';
										echo'		</script>';
										
										
										//}	
										
										
									}
									else{
									echo "<button class='box image-block col-md-3 col-sm-3 col-xs-4 col-xxs-6 col-xxxs-6 col-xxxxs-12' onClick=doToggel('".$vButton['arduino'].'-'.$vButton['pin']."')>";
									echo "<p class='content'>".$vButton['naam']."</br>";
									echo "<i id='".$vButton['arduino'].'-'.$vButton['pin']."' class='fa ".$vButton['glyphicon_code']." fa-4'></i>";
									echo "<p hidden class='id'>".$vButton['arduino']."-".$vButton['pin']."</p>";
									echo "</p>";
									echo "</button>";
									}

								}
							echo "</div>";
							
							
						if($row['id'] == 4){
							
							$boolradio = true;
							include 'radiomodule.php';
							echo "</div>";
						 // echo "</div>";	//added 
						}	
							
							
							echo "</div>";
						
						
							
					echo "</div>";		
					
				}
				
				
				// if($boolradio == false){
					// echo "<div>";
						// // echo "<div class='container-fluid'>";
						// // // include 'radiomodule.php';
						// // echo "</div>";	
					// echo "</div>";	
				// }
				}
				
				
				echo "</div>";	
				echo "</div>";	
					
					?>
				

	 
    </div><!-- /.container -->
   



    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="js/jasny-bootstrap.min.js"></script>
	<script src="js/easyResponsiveTabs.js"></script>
	<script src="js/roundslider.min.js"></script>
	<script type="text/javascript" src="js/mqttws31.js"></script>
	<!-- <script src="js/iRule.js" java_var_1="Kelder"></script> -->
	<script type="text/javascript">
		var MQTT_ip_address = "<?php echo $config['MQTT_ip_address']; ?>"; 
		var MQTT_port = "<?php echo $config['MQTT_port']; ?>"; 
		var vButtonArray = new Array();
	</script>
	<script src="js/iRule.js"></script>
  </body>
</html>
