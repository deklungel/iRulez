<?PHP
require_once('config.php');         

// Database connection                                   
$mysqli = mysqli_init();
$mysqli->options(MYSQLI_OPT_CONNECT_TIMEOUT, 5);
$mysqli->real_connect($config['db_host'],$config['db_user'],$config['db_password'],$config['db_name']); 

$qry = $mysqli->query("SELECT * FROM Settings");
while($row = $qry->fetch_assoc()) {
	$config[$row["Setting"]] = $row["value"];
}

if(isset($_POST['AddButton'])){
	$sql = "INSERT INTO Monitor_Devices (IP) VALUES ('".$_POST['ip']."')";
	processSQL($sql);
}
elseif(isset($_POST['RemoveButton'])){
	$sql = "DELETE FROM Monitor_Devices  WHERE IP = '".$_POST['ip']."'";
	processSQL($sql);
}



if (!empty($_SERVER['HTTP_CLIENT_IP'])) {
    $ip = $_SERVER['HTTP_CLIENT_IP'];
} elseif (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
    $ip = $_SERVER['HTTP_X_FORWARDED_FOR'];
} else {
    $ip = $_SERVER['REMOTE_ADDR'];
}

$clientSQL = mysqli_query($mysqli,"SELECT * FROM Monitor_Devices WHERE IP='".$ip."'");

if (mysqli_num_rows($clientSQL) == 0) {
   $add = true;
}
else{
	$add = false;
}

mysqli_close($mysqli);


function processSQL($sql){
	global $mysqli, $fail;
	// echo $sql;
	if($fail == false){
		if(mysqli_query($mysqli, $sql)){
			// echo " - success</br>";
		}
		else{
			echo $sql." - fail</br>";
			echo "Error updating record: " . mysqli_error($mysqli). "</br>";
			$fail = true;
		}
	}
}

?>

<html>
<head>
<title>iRulez - Monitoring</title>
	<link rel="stylesheet" href="css/edit_style.css" type="text/css" media="screen">
</head>
<body id='mobile'>
<h1>Monitoring</h1>
<form action="" method="post">
<?PHP
echo '<input type="hidden" name="ip" value="'.$ip.'">';
if($add){
	echo '<button type="submit" name="AddButton" class="buttonAdd">Add</button>';
}
else{
	echo '<button type="submit" name="RemoveButton" class="buttonRemove">Remove</button>';
}
?>
<form>
</body>
</html>