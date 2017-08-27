<?php
$qry = $mysqli->query("SELECT * FROM Settings");
while($row = $qry->fetch_assoc()) {
	$config[$row["Setting"]] = $row["value"];
}

$qry = $mysqli->query("SELECT * FROM html_Language");
while($row = $qry->fetch_assoc()) {
	$language[$row["TAG"]] = $row[$config["Language"]];
}


?>

