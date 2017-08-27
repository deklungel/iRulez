<?php
//Version 1.0
if (isset($_GET['reload'])){
echo '<div id="notConnected"><h1 >Connecting to MQTT</h1></div>';
		echo '<script src="js/jquery-2.2.3.min.js"></script>';
		echo '<script type="text/javascript" src="js/mqttws31.js"></script>';
   		echo'<script type="text/javascript">';
			echo "var MQTT_ip_address = \"".$config['MQTT_ip_address']."\";";
			echo "var MQTT_port =\"".$config['MQTT_port']."\";";
			echo "var service =\"".$service."\";";
echo	"</script>";
echo	'<script src="js/iRule_reload.js"></script>';
}
?>