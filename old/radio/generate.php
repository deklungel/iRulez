 <script src="js/jquery-2.2.3.min.js"></script>
<div id="wrap">
<?php
/*
 * Playlist generator
 *
 * @version 2015-08-30
 * @author François LASSERRE <choiz@me.com>
 * @license GNU GPL {@link http://www.gnu.org/licenses/gpl.html}
 */

require 'station.php';
require 'playlist.php';

if (isset($_POST['Create'])){

	
	
	$list = (isset($_POST["list"]) ? explode(",", $_POST["list"]) : "" );
	$id = (isset($_POST["id"]) ? $_POST["id"] : "" );
	$list2 = (isset($_POST["list2"]) ? explode("|", $_POST["list2"]) : "" );
	$naam = (isset($_POST["naam"]) ? $_POST["naam"] : "" );
	$omschrijving = (isset($_POST["omschrijving"]) ? $_POST["omschrijving"] : "" );	
	$url = (isset($_POST["url"]) ? $_POST["url"] : "" );
	if(!empty($list) || !empty($list2)){
		var_dump($list);
		var_dump($list2);
		
		$sql = "DELETE FROM html_Radio_playlist_Zender WHERE html_Radio_playlist = ".$id;
		mysqli_query($mysqli, $sql);
		
		
		$station = new Station($naam, $omschrijving, $url);
		for ($i = 0; $i < count($list); $i++) {	
			if($list2[$i] != ""){
				$station->addServer($list[$i]);		
				
				$sql = "INSERT INTO html_Radio_playlist_Zender (Naam, url, html_Radio_playlist) VALUES ('".$list2[$i]."', '".$list[$i]."', ".$id.")";
				// echo ($sql."</br>");
				mysqli_query($mysqli, $sql);
			}
		}
		
		$playlist = new Playlist($station, 'm3u');
		$playlist->generate();
		header("Location: edit.php?table=PlayList");
	}
	else{
		echo "No values";
	}
	
}
else{
	echo "Geen Create";
}
?>
</div>