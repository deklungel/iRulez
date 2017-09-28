<?php
	// The code below creates the class
	class ControlMessage {
		// Creating some properties (variables tied to an object)
		public $Source = "None";
		public $MAC;
		public $ByteH = array();
		public $ByteL = array();
		
		
		// Assigning the values
		public function __construct($Source, $MAC, $ByteHStr, $ByteLStr)
		{
			
			$this->Source = $Source;
			$this->MAC = $MAC;
			for ($i = 0; $i < strlen($ByteHStr); $i++){
				array_push($this->ByteH, (int)$ByteHStr[$i]);
				echo (int)$ByteHStr[$i];
			}
			for ($i = 0; $i < strlen($ByteLStr); $i++){
				array_push($this->ByteL, (int)$ByteLStr[$i]);
			}
		}
		public function converToBinary($string)
		{
			$value = unpack('H*', $string);
			$binary = str_pad(base_convert($value[1], 16, 2),strlen($string)*8,'0',STR_PAD_LEFT);

			var_dump($binary);

			$bytes = str_split($binary,8);	
			return $bytes;			
		}
		
		// Creating a method (function tied to an object)
		public function toString() {
			return $this->Source . " " . $this->MAC . " " . $this->ByteH . " " . $this->ByteL;
		}
		public function toJSON()
		{
			return json_encode($this);
		}
		public function toBinary()
		{
			return utf8_encode(json_encode($this));
		}
	  }
?>