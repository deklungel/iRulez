<?php
header("Content-Type:application/json");
// ENTRY point for API
// We'd rather have some RESTFULness but for now, this should do
if(!empty($_GET['action']))
{
	// TODO: "if authenticated"
	switch($_GET['action'])
	{
		case "getdevices":
			getDevices();
			break;
		case "getdevice":
			if(!empty($_GET['mac']))
			{
				getDevice($_GET['mac']);
			}
			else
			{
				response(400,"Invalid parameter", null);
			}
			break;
		case "triggerdevicestate":
			triggerDeviceState();
			break;
		default:
			response(400,"Invalid action", null);
	}
}
else
{
	response(400,"Invalid action", null);
}

// Final point, trigger response to the client
function response($status,$message,$data)
{
	header("HTTP/1.1 ". $status ." ".$message);
	echo json_encode($data);
}

function getDevices()
{
	include('../lib/class.database.device.php'); // required 
	$dbdevices = new DBDevice();
	$devices = $dbdevices->getDevices();
	response(200, "Devices found", $devices);
}
function getDevice($mac)
{
	include('../lib/class.database.device.php'); // required 
	$dbdevices = new DBDevice();
	$device = $dbdevices->getDevice($mac);
	response(200, "Device found", $device);	
}
function triggerDeviceState()
{
	try
	{
		$json_params = file_get_contents("php://input"); // Read JSON in POST variables
		$decoded_params = json_decode($json_params, true); // interpret JSON into Array
		if(array_key_exists("L",$decoded_params) && array_key_exists("H",$decoded_params) && array_key_exists("Mac",$decoded_params))
		{
			include('../lib/class.mosquitto.device.php'); // required 

			$mqtt = new MQTTDevice();
			$mqtt->requestNewState($decoded_params["Mac"],$decoded_params["H"],$decoded_params["L"]);
			// We have all we need
			response(200, "Device State trigger valid", true);
		}
		else
		{
			// Invalid input data
			response(400, "Device State trigger invalid", $decoded_params);
		}
	} catch (Exception $e) {
		echo $e;
		// Invalid input data
		response(400, "Device State trigger error", $e);
	}
}