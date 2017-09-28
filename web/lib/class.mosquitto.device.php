<?php
include('../lib/class.mosquitto.php'); // required 
include('../lib/class.controlmessage.php'); // required 

// The code below creates the class
class MQTTDevice {
	public function requestNewState($mac,$H,$L)
	{
		$mqtt = MQTT::getInstance();
		$controlmessage = new ControlMessage("requestNewState", $mac,$H,$L);
		$mqtt->publishMessage("/CONTROL", $controlmessage->toJSON());
	}
  }
?>