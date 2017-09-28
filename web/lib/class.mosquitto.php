<?php
/*
* Mysql database class - only one connection alowed
*/
include('../config/config_mosquitto.php'); // required 

class MQTT {
	private $_client;
	private static $_instance; //The single instance
	private $_host = config_mosquitto_host;
	private $_port = config_mosquitto_port;
	private $_keepalive = config_mosquitto_keepalive;
	
	/*
	Get an instance of the Database
	@return Instance
	*/
	public static function getInstance() {
		if(!self::$_instance) { // If no instance then make one
			self::$_instance = new self();
		}
		return self::$_instance;
	}

	// Constructor
	private function __construct() {
		$this->_client = new Mosquitto\Client();
	}
	

	// Magic method clone is empty to prevent duplication of connection
	private function __clone() { }

	// Get client for reasons
	public function getClient() {
		return $this->_client;
	}
	public function publishMessage($queue,$message)
	{
		$this->_client->connect($this->_host, $this->_port,$this->_keepalive);
		$this->_client->publish($queue, $message);
		$this->_client->disconnect();
	}
}
?>
