<?php
//Version 1.3

if(empty($_GET["table"]))
{
	$page="vButton";
}
else{
	$page=$_GET["table"];
}


require_once('config.php');         

// Database connection                                   
$mysqli = mysqli_init();
$mysqli->options(MYSQLI_OPT_CONNECT_TIMEOUT, 5);
$mysqli->real_connect($config['db_host'],$config['db_user'],$config['db_password'],$config['db_name']); 


require_once('language.php'); 
?>

<!DOCTYPE html>
<html lang="en">
  <head>
	<title>iRulez - Edit</title>
	<link rel="icon" type="image/png" href="favicon.ico" />
	<link rel="stylesheet" href="css/edit_style.css" type="text/css" media="screen">
	<link rel="stylesheet" href="css/responsive.css" type="text/css" media="screen">
	<link rel="stylesheet" href="css/font-awesome-4.1.0/css/font-awesome.min.css" type="text/css" media="screen">
</head>
  </head>
  <body>
	 <div id='cssmenu'>
	 <a href="index.php"><img src="images/iRulez_Logo.png" alt='i' id="iRulez_Logo">Rulez</a>
	<ul>
		<li class='active'><a href="?table=vButton"><?PHP echo ucfirst($language['Edit_menu1']); ?></a></li>
		<li><a href="?table=vButton_actions"><?PHP echo ucfirst($language['Edit_menu2']); ?></a></li>
		<li><a href="?table=timer"><?PHP echo ucfirst($language['Edit_menu3']); ?></a></li>
		<li><a href="?table=outputs"><?PHP echo ucfirst($language['Edit_menu4']); ?></a></li>
		<li><a href="?table=devices"><?PHP echo ucfirst($language['Edit_menu5']); ?></a></li>
		<?PHP
		if($page == 'monitor' || $page == 'owntracks_waypoints' || $page == 'owntracks_action' || $page == 'owntracks_groups'){
			echo '<li class="has-sub open"><a href="?table=monitor">'.ucfirst($language['Edit_menu6']).'</a>';
			echo '<ul>';
		}
		else{
			echo '<li class="has-sub"><a href="?table=monitor">'.ucfirst($language['Edit_menu6']).'</a>';
			echo '<ul style="display: none;">';
		}
		?>
				<li><a href="?table=monitor"><?PHP echo ucfirst($language['Edit_menu_Sub6_1']); ?></a></li>
				<li><a href="?table=owntracks_waypoints"><?PHP echo ucfirst($language['Edit_menu_Sub6_2']); ?></a></li>
				<li><a href="?table=owntracks_action"><?PHP echo ucfirst($language['Edit_menu_Sub6_3']); ?></a></li>
				<li><a href="?table=owntracks_groups"><?PHP echo ucfirst($language['Edit_menu_Sub6_4']); ?></a></li>
			</ul>
		</li>
		<?PHP
		if($page == 'radio' || $page == 'radiozender' || $page == 'PlayList'){
			echo '<li class="has-sub open"><a href="?table=radio">'.ucfirst($language['Edit_menu7']).'</a>';
			echo '<ul>';
		}
		else{
			echo '<li class="has-sub"><a href="?table=radio">'.ucfirst($language['Edit_menu7']).'</a>';
			echo '<ul style="display: none;">';
		}
		?>
				<li><a href="?table=radio"><?PHP echo ucfirst($language['Edit_menu_Sub7_1']); ?></a></li>
				<li><a href="?table=radiozender"><?PHP echo ucfirst($language['Edit_menu_Sub7_1']); ?></a></li>
				<li><a href="?table=PlayList"><?PHP echo ucfirst($language['Edit_menu_Sub7_3']); ?></a></li>
			</ul>
		</li>
				<?PHP
		if($page == 'verdiepen' || $page == 'spaces'){
			echo '<li class="has-sub open"><a href="?table=radio">'.ucfirst($language['Edit_menu8']).'</a>';
			echo '<ul>';
		}
		else{
			echo '<li class="has-sub"><a href="?table=radio">'.ucfirst($language['Edit_menu8']).'</a>';
			echo '<ul style="display: none;">';
		}
		?>
				<li><a href="?table=verdiepen"><?PHP echo ucfirst($language['Edit_menu_Sub8_1']); ?></a></li>
				<li><a href="?table=spaces"><?PHP echo ucfirst($language['Edit_menu_Sub8_2']); ?></a></li>
			</ul>
		</li>
		
		<li><a href="?table=statistics"><?PHP echo ucfirst($language['Edit_menu_Sub9']); ?></a></li>
		<?PHP
		if($page == 'settings' || $page == 'version' || $page == 'services' || $page == 'backup'){
			echo '<li class="has-sub open"><a href="#">'.ucfirst($language['Edit_menu10']).'</a>';
			echo '<ul>';
		}
		else{
			echo '<li class="has-sub"><a href="?table=settings">'.ucfirst($language['Edit_menu10']).'</a>';
			echo '<ul style="display: none;">';
		}
		?>
				<li><a href="?table=settings"><?PHP echo ucfirst($language['Edit_menu_Sub10_1']); ?></a></li>
				<li><a href="?table=version"><?PHP echo ucfirst($language['Edit_menu_Sub10_2']); ?></a></li>
				<li><a href="?table=services"><?PHP echo ucfirst($language['Edit_menu_Sub10_3']); ?></a></li>
				<li><a href="?table=backup"><?PHP echo ucfirst($language['Edit_menu_Sub10_4']); ?></a></li>
				<?PHP if($config['loglevel']=="debug"){echo '<li><a href="?table=testbuttons">'.ucfirst($language['Edit_menu_Sub10_5']).'</a></li>';}?>
			</ul>
		</li>
		
    </ul>
	  </div>
	  <div id="watermark"><img id="iRulez_watermark" src="images/iRulez_Logo.png" alt='i'></img></div>
	  <div class='container'>
	  
			<?php
			if ($page == 'vButton_actions')
			{
				$service = 'Core';
				include("reload.php");
			}
			if ($page == 'vButton' || $page == 'owntracks_waypoints' || $page == 'owntracks_action' || $page == 'owntracks_groups' || $page == 'PlayList' || $page == 'devices' || $page == 'settings' || $page == 'verdiepen' || $page == 'spaces' || $page == 'vButton_actions' || $page == 'outputs' || $page == 'radio' || $page == 'radiozender' || $page == 'monitor')
			{
				include("languageJS/".$page.".php");
				include("wrap/wrap_".$page.".php");
				echo '<script src="js/'.$page.'.js" ></script>';
				echo '<script src="js/table_behaviour.js" ></script>';
				if ($page != 'outputs' && $page != 'settings' &&  $page != 'vButton_actions'){
					include("add_form/add_form_".$page.".php");
				}
			}
			else if ($page == 'services')
			{
				include("services.php");
			}
			else if ($page == 'backup')
			{
				include("backup.php");
			}
			else if ($page == 'wizard')
			{
				include("wizard.php");
			}
			else if ($page == 'editPlayList')
			{
				include("createPlayList.php");
			}
			else if ($page == 'createPlaylist')
			{
				include("radio/generate.php");
			}
			else if ($page == 'update')
			{
				include("update_actions.php");
			}
			else if ($page == 'update2')
			{
				include("update_actions2.php");
			}
			else if ($page == 'timer')
			{
				$service = 'Timer';
				include("reload.php");
				include("timer.php");
			}
			else if ($page == 'statistics')
			{
				include("statistics.php");
			}
			else if ($page == 'update_Timer')
			{
				include("timer_update.php");
			}
			else if ($page == 'stats_popup_day')
			{
				include("stats_popup_day.php");
			}
			else if ($page == 'stats_popup_week')
			{
				include("stats_popup_week.php");
			}
			else if ($page == 'stats_popup_month')
			{
				include("stats_popup_month.php");
			}
			else if ($page == 'version')
			{
				include("version.php");
			}
			else if ($page == 'testbuttons')
			{
				include("testbuttons.php");
			}
			
			?>
			

	  </div>
  </body>
  <footer>
	<script src="js/edit_menu.js"></script>
  </footer>
 </html>