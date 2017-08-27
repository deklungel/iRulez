<?php
//Version 1.0
	require_once "WebService/lib/nusoap.php";
	require_once('config.php');  

	
// Database connection                                   
$mysqli = mysqli_init();
$mysqli->options(MYSQLI_OPT_CONNECT_TIMEOUT, 5);
$mysqli->real_connect($config['db_host'],$config['db_user'],$config['db_password'],$config['db_name']); 

	$qry = $mysqli->query("SELECT * FROM Settings");
	while($row = $qry->fetch_assoc()) {
		$config[$row["Setting"]] = $row["value"];
	}


	$client = new nusoap_client($config['Update_Server']);

	$error = $client->getError();
	if ($error) {
		echo "<h2>Constructor error</h2><pre>" . $error . "</pre>";
	}
	
	$result = $client->call("getVersion");
	if ($client->fault) {
		echo "<h2>Fault</h2><pre>";
		print_r($result);
		echo "</pre>";
	}
	else {
		$error = $client->getError();
		if ($error) {
			echo "<h2>Error</h2><pre>" . $error . "</pre>";
		}
		else {
			//echo var_dump($result);
		}
	}


if (!$mysqli->query("TRUNCATE TABLE html_versions")) {
    echo "Table clear failed: (" . $mysqli->errno . ") " . $mysqli->error;
}
else{
	//echo "Tabel html_versions cleared</br>";
	  while ($record = current($result)) {
			$tmp= key($result);
			if (key($result) == "Website"){
				$tmp = "Website/html";
			}
			while ($record2 = current($record)) {
				$tmp2 = key($record);
					while ($record3 = current($record2)) {
						$file = $tmp."/".$tmp2."/".key($record2);
						$file = str_replace("html/html", "html", $file);
						$version = $record3[0];
						
						$sql = "INSERT INTO html_versions VALUES ('".$file."','".$version."')";
							if ($mysqli->query($sql) === TRUE) {
								//echo "New record created successfully</br>";
							} else {
								echo "Error: " . $sql . "<br>" . $mysqli->error;
							}
						
						next ($record2);
					}
				next ($record);
			}

		 $tmp="";
		 next($result);
	 }
	 header( "refresh:0;url=edit.php?table=version" );
}


$mysqli->close();

?>