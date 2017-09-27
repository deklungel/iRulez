<?php
include('../lib/class.database.php'); // required 
include('../lib/class.device.php'); // required 


// The code below creates the class
class DBDevice {
	public function getDevices()
	{
		$devices = array(); // return object

		// Get Database instance
		$db = Database::getInstance();
		$mysqli = $db->getConnection(); 
		$sql_query = "SELECT id,MAC, LastModified, Created, State FROM devices";
//		if(TRACEMODE==1) echo $sql_query;

		if ($result = $mysqli->query($sql_query)) {
			/* fetch associative array */
			while ($row = $result->fetch_assoc()) {
				$device = new Device($row["id"], $row["MAC"],$row["State"], $row["Created"], $row["LastModified"]);
				array_push($devices, $device);
			}
			/* free result set */
			$result->free();
		}
		return $devices;
	}
  }
?>