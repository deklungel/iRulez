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
		default:
			response(400,"Invalid action", null);
	}
}
else
{
	response(400,"Invalid action", null);
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
function response($status,$message,$data)
{
	header("HTTP/1.1 ". $status ." ".$message);
	echo json_encode($data);
}