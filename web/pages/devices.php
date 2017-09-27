<html>
<head>
	<title>Demo reading data from Mysql</title>
	
	<link rel="stylesheet" type="text/css" href="/css/irulez.css">
	<script
  src="https://code.jquery.com/jquery-3.2.1.js"
  integrity="sha256-DZAnKJ/6XZ9si04Hgrsxu/8s717jcIzLy3oi35EouyE="
  crossorigin="anonymous"></script>
  
	<script type="text/Javascript" src="/js/iRulez.js"></script>
	<script type="text/Javascript">
		/* This section is specific to this page. Generic JavaScript code should be added into iRulez for global access */
		function getDevices()
		{
			$(".devices").html("Loading...");
			iRulez.Log("iRulez", "loading items async");
			
			iRulez.Data.getDevices(
							function(result) // the result that comes back
							{
								iRulez.Log("iRulez", "Items loaded");
								renderDevices(result);
							});
		}
		function renderDevices(devices)
		{
			var _deviceHTML = ""; // intermediate HTML, we do this stringbased as Jquery tries to do DOM stuff before we're done elsewya
			for(var d in devices)
			{
				iRulez.Log("iRulez", JSON.stringify(devices[d])); // send it to log so we can trace
				_deviceHTML += renderDevice(devices[d]); // render the device layer
			}
			$(".devices").html(_deviceHTML); // to the browser!
			$(".devices .device").click(function()
			{
				alert("What you gonna do with " + $(this).data("mac"));
			});
		}
		function renderDevice(device) // visual representation of this device
		{
			return "<div class='device' data-mac='"+ device.MAC +"'>" +
						"<b>Mac:</b> " + device.MAC + "<br />" +
						"<b>State:</b> " + device.State + "<br />"+
						"<b>Created:</b> " + device.Created + "<br />"+
						"<b>LastModified:</b> " + device.LastModified + "<br />"+
					"</div>";
		}
	</script>
  </head>
<body>
<h1>Inline database</h1>
<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

include('../lib/class.database.device.php'); // required 
$dbdevices = new DBDevice();
$devices = $dbdevices->getDevices();
foreach ($devices as $device) {
	echo $device->toJson();
}
?>
<h1>Javascript and service</h1>
<button onclick="getDevices()">Click to load devices</button>
<div class="devices">
</div>
</body>
</html>