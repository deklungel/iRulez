//Version 1.0
$(document).ready(function() { 
	RemoveConnectionDIV();
	reload();
	});
	
	var client;
	var clientID = "MIR-websocket"+Math.floor(Math.random()*100); // 0 - 99

	function reload(){
		if (confirm('Wil je de service ' +service+' herstarten?')) {
			AddConnectionDIV()
			doConnect();
		} 
	}
	
	function doConnect() {
		client = new Messaging.Client(MQTT_ip_address, parseInt(MQTT_port), clientID);
		client.onConnect = onConnect;
		// client.onMessageArrived = onMessageArrived;
		client.onConnectionLost = onConnectionLost;
		client.connect({onSuccess:onConnect,onFailure:onConnectionLost});
	}
	function onConnect() {
		RemoveConnectionDIV()
		publishReload(service);
		
	}
	function RemoveConnectionDIV(){
		var div = document.getElementById("notConnected");
		div.style.display = "none";
	}
	
	// function onMessageArrived(message) {
		// var arr = message.destinationName.split("/");
		// var arduino = arr[0].replace("arduino","");
		// var pin = arr[1].replace("vbutton","");
		// if (message.payloadString == "H")
		// {
			// jQuery("#"+arduino+"-"+pin).addClass('active');
		// }
		// else if (message.payloadString == "L")
		// {
			// jQuery("#"+arduino+"-"+pin).removeClass('active');
		// }
				
	// }
	function onConnectionLost(responseObject) {
		AddConnectionDIV()

		if (responseObject.errorCode !== 0)
			alert(client.clientId+"\n"+responseObject.errorCode);
		
		doConnect()
	}
	function AddConnectionDIV(){
		var div = document.getElementById("notConnected");
		div.style.display = "block";
	}
	
	function publishReload(service) {
		message = new Messaging.Message(status);
		message.destinationName = service+"/service/restart";
		message.retained=false;
		client.send(message);
	}
	

 
  
	
  		
	

		