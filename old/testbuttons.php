<?php
//Version 1.0
require_once('config.php'); 
?>
<div id="notConnected"><h1 >Connecting to MQTT</h1></div>

<input id='publish' type="text" name="publish" placeholder="Toppic"><input id='payload' type="text" name="payload" placeholder="payload"><button onClick=doPublish()>Publish</button>

<?PHP
// Database connection                                   
$mysqli = mysqli_init();
$mysqli->options(MYSQLI_OPT_CONNECT_TIMEOUT, 5);
$mysqli->real_connect($config['db_host'],$config['db_user'],$config['db_password'],$config['db_name']); 

$Buttons = mysqli_query($mysqli,"SELECT naam, arduino, pin FROM Core_Arduino_Outputs");

echo "<table>";
echo "<tr><th>Toggel</th><th>Button H</th><th>Button L</th><th>Relais status</th><th>Button Status Low</th><th>Value</th></tr>";
while($Button = mysqli_fetch_assoc($Buttons)) {
	echo "<tr>";
				echo "<td><button onClick=doToggel('".$Button['arduino']."-".$Button['pin']."')>";
				echo $Button['naam']." Toggel";
				echo "</button></td>";
				echo "<td><button onClick=TestL('".$Button['arduino']."-".$Button['pin']."')>";
				echo $Button['naam']." L";
				echo "</button></td>";
				echo "<td><button onClick=TestH('".$Button['arduino']."-".$Button['pin']."')>";
				echo $Button['naam']." H";
				echo "</button></td>";
				echo "<td align='center'><input id='".$Button['arduino']."-".$Button['pin']."' type='checkbox' name='".$Button['arduino']."-".$Button['pin']."' value='0' disabled readonly></td>";
				echo "<td align='center'><input id='B-".$Button['arduino']."-".$Button['pin']."' type='checkbox' name='".$Button['arduino']."-".$Button['pin']."' value='1' disabled readonly></td>";
				echo "<td align='center'><input id='D-".$Button['arduino']."-".$Button['pin']."' type='text' name='".$Button['arduino']."-".$Button['pin']."' value='' disabled readonly></td>";
				echo "<p hidden class='id'>".$Button['arduino']."-".$Button['pin']."</p>";
	echo "</tr>";
}
echo "<table>";
?>
	<script src="js/jquery-2.2.3.min.js"></script>
	<script type="text/javascript" src="js/mqttws31.js"></script>
	<script type="text/javascript">
		var MQTT_ip_address = "<?php echo $config['MQTT_ip_address']; ?>"; 
		var MQTT_port = "<?php echo $config['MQTT_port']; ?>"; 
	</script>
	<script src="js/iRule_Test.js"></script>