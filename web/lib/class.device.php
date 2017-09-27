<?php
	// The code below creates the class
	class Device {
		// Creating some properties (variables tied to an object)
		public $id = true;
		public $MAC;
		public $State;
		public $LastModified;
		public $Created;
		
		
		// Assigning the values
		public function __construct($id, $MAC, $State, $Created, $LastModified)
		{
			$this->id = $id;
			$this->MAC = $MAC;
			$this->State = $State;
			$this->Created = $Created;
			$this->LastModified = $LastModified;
		}
		
		// Creating a method (function tied to an object)
		public function toString() {
			return $this->id . " " . $this->MAC . " " . $this->State . " " . $this->Created . " " . $this->LastModified;
		}
		public function toJSON()
		{
			return json_encode($this);
		}
	  }
?>