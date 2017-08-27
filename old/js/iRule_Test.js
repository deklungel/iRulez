//Version 1.0
$(document).ready(function() { 
		doConnect();
	});
	
	var client;
	var clientID = "MIR-websocket"+Math.floor(Math.random()*100); // 0 - 99

	function doConnect() {
		client = new Messaging.Client(MQTT_ip_address, parseInt(MQTT_port), clientID);
		client.onConnect = onConnect;
		client.onMessageArrived = onMessageArrived;
		client.onConnectionLost = onConnectionLost;
		client.connect({onSuccess:onConnect,onFailure:onConnectionLost});
	}
	function onConnect() {
		RemoveConnectionDIV()
		var x = document.getElementsByClassName("id");
		for (var i = 0; i < x.length; i++) {
			doSubscribe(x[i].innerHTML)
		}	
	}
	function RemoveConnectionDIV(){
		var div = document.getElementById("notConnected");
		div.style.display = "none";
	}
	
	function doSubscribe(vButton) {
			var arrArduinovButton = vButton.split("-");
			client.subscribe("arduino"+arrArduinovButton[0]+"/relais"+arrArduinovButton[1]+"/status");
			client.subscribe("arduino"+arrArduinovButton[0]+"/dimmer"+arrArduinovButton[1]+"/status");
		    client.subscribe("arduino"+arrArduinovButton[0]+"/button"+arrArduinovButton[1]+"/status");
	}
	function doPublish(){
		if(document.getElementById('publish').value != "" && document.getElementById('payload').value != ""){
			if(confirm("Are you sure you want to Publish: "+document.getElementById('publish').value+"/"+document.getElementById('payload').value)) {
				message = new Messaging.Message(document.getElementById('payload').value);
				message.destinationName = document.getElementById('publish').value;
				message.retained=false;
				client.send(message);
			}
		}
		else{
			alert("Topic and/or Payload is empty!")
		}
	}
	function onMessageArrived(message) {
		var arr = message.destinationName.split("/");
		if(arr[1].includes("button")){
			var arduino = arr[0].replace("arduino","");
			var pin = arr[1].replace("button","");
			var payload = message.payloadString
			if (payload == "H")
			{
				document.getElementById("B-"+arduino+"-"+pin).checked = false;
			}
			else if (payload == "L")
			{
				document.getElementById("B-"+arduino+"-"+pin).checked = true;
			}
		
		}
		else{
			var arduino = arr[0].replace("arduino","");
			var pin = arr[1].replace("relais","");
			var dimmer = arr[1].replace("dimmer","");
			var payload = message.payloadString
			if (payload == "H")
			{
				document.getElementById(arduino+"-"+pin).checked = true;
			}
			else if (payload == "L")
			{
				document.getElementById(arduino+"-"+pin).checked = false;
			}
			else
			{
				if(dimmer < 10){
				document.getElementById("D-"+arduino+"-"+dimmer).value = payload;
				}
			}	
		}
		
				
	}
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
	
	function doToggel(vButton) {
		var arrArduinovButton = vButton.split("-");
			publish(arrArduinovButton,"L")
			publish(arrArduinovButton,"H")
	}
	function publish(arrArduinovButton,status) {
		message = new Messaging.Message(status);
		message.destinationName = "arduino"+arrArduinovButton[0]+"/button"+arrArduinovButton[1]+"/status";
		message.retained=false;
		client.send(message);
	}
	
	function TestH(vButtonH){
		var arrArduinovButton = vButtonH.split("-");
			publish(arrArduinovButton,"H")
	}
	function TestL(vButtonL){
		var arrArduinovButton = vButtonL.split("-");
			publish(arrArduinovButton,"L")
	}

  
	
  		
	

		