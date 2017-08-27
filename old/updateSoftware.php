<?php
//Version 1.2
require_once "WebService/lib/nusoap.php";
require_once('config.php'); 

$mysqli = mysqli_init();
$mysqli->options(MYSQLI_OPT_CONNECT_TIMEOUT, 5);
$mysqli->real_connect($config['db_host'],$config['db_user'],$config['db_password'],$config['db_name']); 

	$qry = $mysqli->query("SELECT * FROM Settings");
	while($row = $qry->fetch_assoc()) {
		$config[$row["Setting"]] = $row["value"];
	}

function ssl_decrypt($source,$type,$key){
// The raw PHP decryption functions appear to work
// on 128 Byte chunks. So this decrypts long text
// encrypted with ssl_encrypt().

$maxlength=128;
$output='';
while($source){
  $input= substr($source,0,$maxlength);
  $source=substr($source,$maxlength);
  if($type=='private'){
    $ok= openssl_private_decrypt($input,$out,$key);
  }else{
    $ok= openssl_public_decrypt($input,$out,$key);
  }
       
  $output.=$out;
}
return $output;

}


function GetFile($client,$filename,$pubKey,$privKey){
	$encoded = $client->call("downloadFile",array($filename,$pubKey));

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
		//Decrypt the data using the private key and store the results in $decrypted
		$decode = base64_decode($encoded[0]); 
		$decrypted = ssl_decrypt($decode,'private',$privKey);
		$location = "/var/www/".$encoded[1];  		// Mention where to upload the file
		if ($decrypted != ""){
			file_put_contents($location, $decrypted);
			echo "File ".$filename." has been updated</br>";
			return "success";
		}
		else{
			echo "File not updated";
			echo $filename;
			return "error";
		}
	}
}

}

$keysize = 1024;
$ssl = openssl_pkey_new (array('private_key_bits' => $keysize));
// Create the private and public key

// Extract the private key from $res to $privKey
openssl_pkey_export($ssl, $privKey);

// Extract the public key from $res to $pubKey
$pubKey = openssl_pkey_get_details($ssl);
$pubKey = $pubKey["key"];


$client = new nusoap_client($config['Update_Server']);

$error = $client->getError();
if ($error) {
	echo "<h2>Constructor error</h2><pre>" . $error . "</pre>";
}

if(isset($_POST['update'])){
	$result =  GetFile($client,$_POST['update'],$pubKey,$privKey);
	if($result = "success"){
		echo "You will be redirected to the version overview. If not click <a href='edit.php?table=version'>here</a>";
	//	header( "refresh:2;url=edit.php?table=version" );
	}
	else{
		echo "error";
	}
}
elseif(isset($_POST['updateAll'])){
	$pieces = explode("|",$_POST['updateAll']);
	$error = false;
	for ($i = 0; $i <sizeof($pieces); $i++){
		$result =  GetFile($client,$pieces[$i],$pubKey,$privKey);
		if($result == "error"){
			$error = true;
		}
	}
	if($error == false){
		echo "You will be redirected to the version overview. If not click <a href='edit.php?table=version'>here</a>";
		header( "refresh:2;url=edit.php?table=version" );
	}
	else{
		echo "error";
	}
	
}


?>