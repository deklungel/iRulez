//Version 1.8

$(document).ready(function() { 
		doConnect();
		var y = document.getElementsByClassName("radioId");
		for (var i = 0; i < y.length; i++) {
			startScrolling(y[i].innerHTML);
		}
	});
	
	var client;
	var clientID = "MIR-websocket"+Math.floor(Math.random()*100); // 0 - 99
	var LastDimmerMessageSent = 0;
	var LastVolumeMessageSent = 0;
	var timeout = 0;

	function doConnect() {
		client = new Messaging.Client(MQTT_ip_address, parseInt(MQTT_port), clientID,10);
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
		var y = document.getElementsByClassName("radioId");
		for (var i = 0; i < y.length; i++) {
			client.subscribe(y[i].innerHTML+"/status/#");
		}
		var z = document.getElementsByClassName("dimmerId");
		for (var i = 0; i < z.length; i++) {
			var arrArduinovButton = z[i].innerHTML.split("-");
			client.subscribe("WebInterface/arduino"+arrArduinovButton[0]+"/dimmer"+arrArduinovButton[1]+"/status");
		}	
	}
	function RemoveConnectionDIV(){
		var div = document.getElementById("notConnected");
		div.style.display = "none";
		timeout = 0;
	}
	
	function doSubscribe(vButton) {
			var arrArduinovButton = vButton.split("-");
			client.subscribe("arduino"+arrArduinovButton[0]+"/vbutton"+arrArduinovButton[1]+"/status");
	}

	
	function onMessageArrived(message) {
		//alert(LastDimmerMessageSent);
		var d = new Date();
		//alert(d.getTime());
		
		if(message.destinationName.includes("kodi")){	
			var kodi = JSON.parse(message.payloadString);
			var arr = message.destinationName.split("/");
			var kodiID = arr[0];
			if(message.destinationName.includes("volume")&& LastVolumeMessageSent <= d.getTime()){
				//kodi/status/volume/{"kodi_muted": "false", "val": 75}
				$("#Volume-"+kodiID).roundSlider("option", "value", kodi.val);
			}
			else if(message.destinationName.includes("playbackstate")){
				//odi/status/playbackstate/{"kodi_timestamp": 1467883572, "kodi_playbackdetails": {"subtitleenabled": false, "currentaudiostream": {}, "repeat": "off", "currentsubtitle": {}, "speed": 1}, "val": 1, "kodi_state": "started", "kodi_playertype": "audio", "kodi_playerid": 1}
				if(kodi.val == 0){
					//stopped
					//alert ("Stopped");
					jQuery("[id=stop"+kodiID+"]").addClass('active');
					jQuery("[id=play"+kodiID+"]").removeClass('active');
					jQuery("[id=pause"+kodiID+"]").removeClass('active');
					jQuery("[id=youtube"+kodiID+"]").removeClass('active');
					var y = document.getElementsByClassName("marquee"+kodiID);
					y[0].innerHTML = "";
					document.getElementById("radioUrl"+kodiID).value = "";
					var z = document.getElementsByClassName("Time"+kodiID);
					z[0].innerHTML = "";
					startScrolling(kodiID);
				}
				else if(kodi.val == 1){
					//play
					//alert ("Play");
					jQuery("[id=play"+kodiID+"]").addClass('active');
					jQuery("[id=stop"+kodiID+"]").removeClass('active');
					jQuery("[id=pause"+kodiID+"]").removeClass('active');
				}
				else if(kodi.val == 2){
					//pauze
					//alert ("pauze");
					jQuery("[id=pause"+kodiID+"]").addClass('active');
					jQuery("[id=stop"+kodiID+"]").removeClass('active');
					jQuery("[id=play"+kodiID+"]").removeClass('active');
					jQuery("[id=youtube"+kodiID+"]").removeClass('active');
				}
				
			}
			else if(message.destinationName.includes("title")){
				//kodi/status/title/{"kodi_details": {"title": "", "fanart": "", "label": "Qmusic_be_live_96.mp3", "file": "http://icecast-qmusic.cdp.triple-it.nl:80/Qmusic_be_live_96.mp3", "type": "unknown", "thumbnail": "", "streamdetails": {"video": [], "audio": [], "subtitle": []}}, "val": ""}
				var y = document.getElementsByClassName("marquee"+kodiID);
				if (!kodi.kodi_details.label)
				{
					y[0].innerHTML = "";
				}
				else{
					y[0].innerHTML = kodi.kodi_details.label;
					if (kodi.kodi_details.file.search("youtube")  === -1){
						document.getElementById("radioUrl"+kodiID).value = kodi.kodi_details.file;
					}
					else{
						jQuery("[id=youtube"+kodiID+"]").addClass('active');
					}
				}
				startScrolling(kodiID);
			}
			else if(message.destinationName.includes("progress")){
				//"kodi_time": "00:02:54", "kodi_totaltime": "00:56:23", "val": "5.2"}
				var y = document.getElementsByClassName("Time"+kodiID);
				if (kodi.kodi_totaltime == "00:00:00")
				{
					y[0].innerHTML = "";
				}
				else{
					y[0].innerHTML = kodi.kodi_time + "/" + kodi.kodi_totaltime + " ("+ kodi.val +"%)";
				}
			}
		}	
		else if(message.destinationName.includes("WebInterface") && LastDimmerMessageSent <= d.getTime()){
			var arr = message.destinationName.split("/");
			var arduino = arr[1].replace("arduino","");
			var dimmer = arr[2].replace("dimmer","");
			// $("#Dimmer-"+arduino+"-"+dimmer).roundSlider("option", "value", message.payloadString);
			jQuery("[id$='Dimmer-"+arduino+"-"+dimmer+"']").roundSlider("option", "value", message.payloadString);
		}
		else if(message.destinationName.includes("vbutton")){
			var arr = message.destinationName.split("/");
			var arduino = arr[0].replace("arduino","");
			var pin = arr[1].replace("vbutton","");
			if (message.payloadString == "H")
			{
				jQuery("[id="+arduino+"-"+pin+"]").addClass('active');
				vButtonArray[arduino+pin]= "H";
				// if(pin < 10){
					// var value = jQuery("[id=D-"+arduino+"-"+pin+"]").val();
					// alert ("HIGH [id=D-"+arduino+"-"+pin+"]" + value);
				// }
			}
			else if (message.payloadString == "L")
			{
				jQuery("[id="+arduino+"-"+pin+"]").removeClass('active');
				vButtonArray[arduino+pin]= "L";
				// if(pin < 10){
					// var value = jQuery("[id=D-"+arduino+"-"+pin+"]").val();
					// alert ("LOW [id=D-"+arduino+"-"+pin+"]" + value);
				// }
			}				
		}
	}
	function onConnectionLost(responseObject) {
		AddConnectionDIV();
		if (responseObject.errorCode !== 0)
			//alert(client.clientId+"\n"+responseObject.errorCode);
		
		doConnect()
	}
	function AddConnectionDIV(){
		var div = document.getElementById("notConnected");
		div.style.display = "block";
	}
	
	function doToggel(vButton) {
		var arrArduinovButton = vButton.split("-");
			publish(arrArduinovButton,"L");
			publish(arrArduinovButton,"H");
		LastDimmerMessageSent = 0;
	}
	function publish(arrArduinovButton,status) {
		message = new Messaging.Message(status);
		message.destinationName = "arduino"+arrArduinovButton[0]+"/button"+arrArduinovButton[1]+"/status";
		message.retained=false;
		client.send(message);
	}
	function doDimmer(dimmer,arduino) {
		var d = new Date();
		var arr = arduino.split("|");
		message = new Messaging.Message(dimmer.toString());
		var arduino = arr[0].replace(/;$/, "").split(";");
		var dimmer = arr[1].replace(/;$/, "").split(";");
		for (var i = 0; i < arduino.length; i++) {
			message.destinationName = "arduino"+arduino[i]+"/dimmer"+dimmer[i]+"/value";
			message.retained=false;
			client.send(message);
			LastDimmerMessageSent = d.getTime() + 1000; 
		}
	}
	function changeTooltip(e) {
		var val = e.value, speed;
		// if (val < 75) speed = "Low";
		// else if (val < 150) speed = "Medium";
		// else if (val < 200) speed = "High";
		// else speed = "Very High";

		//return val + "" + "<div>" + speed + "<div>";
		return val;
	}
	function startScrolling(id) {

    var marquee = $("#marquee"+id); 
    marquee.css({"overflow": "hidden", "width": "100%"});

    // wrap "My Text" with a span (IE doesn't like divs inline-block)
    marquee.wrapInner("<span>");
    marquee.find("span").css({ "width": "50%", "display": "inline-block", "text-align":"center" }); 
    marquee.append(marquee.find("span").clone()); // now there are two spans with "My Text"

    marquee.wrapInner("<div>");
    marquee.find("div").css("width", "200%");

    var reset = function() {
        $(this).css("margin-left", "0%");
        $(this).animate({ "margin-left": "-100%" }, 7500, 'linear', reset);
    };

    reset.call(marquee.find("div"));
	}
	
	function publishRadio(id){
		var e = document.getElementById("radioUrl"+id);
		var url = e.options[e.selectedIndex].value;
		if (url != ''){
			if(url.search("www.youtube.com") > -1){
				var arr = url.split("/");
				var youtubeId = arr[arr.length - 1];
				youtubeId = youtubeId.replace("watch?v=","");
				var text = '{ "item": { "file":"plugin://plugin.video.youtube/?action=play_video&videoid='+youtubeId+'"}}';
				message = new Messaging.Message(text);
			}
			else{
				message = new Messaging.Message(url);
			}
			message.destinationName = id+"/command/play";
			message.retained=false;
			client.send(message);
		}
	}
	function ChangeVolume(value,id) {
		message = new Messaging.Message(value.toString());
		message.destinationName = id+"/command/volume";
		message.retained=false;
		client.send(message);
		var d = new Date();
		LastVolumeMessageSent = d.getTime() + 1000; 
	}
	function clickPlay(id){
		message = new Messaging.Message("resume");
		message.destinationName = id+"/command/playbackstate";
		message.retained=false;
		client.send(message);
	}
	function clickPause(id){
		message = new Messaging.Message("pause");
		message.destinationName = id+"/command/playbackstate";
		message.retained=false;
		client.send(message);
	}
	function clickStop(id){
		message = new Messaging.Message("stop");
		message.destinationName = id+"/command/playbackstate";
		message.retained=false;
		client.send(message);
	}
	function clickyoutube(id){
		var e = document.getElementById("youtube"+id);
		var url = e.value;
		if (url != ''){
			var arr = url.split("/");
			var youtubeId = arr[arr.length - 1];
			youtubeId = youtubeId.replace("watch?v=","");
			var text = '{ "item": { "file":"plugin://plugin.video.youtube/?action=play_video&videoid='+youtubeId+'"}}';
			message = new Messaging.Message(text);
			message.destinationName = id+"/command/play";
			message.retained=false;
			client.send(message);
		}
	}
	

	// function changeTooltip(e) {
			// var val = e.value, speed;
			// // if (val < 20) speed = "Slow";
			// // else if (val < 40) speed = "Normal";
			// // else if (val < 70) speed = "Speed";
			// // else speed = "Very Speed";

			// return val + "<div onclick='myFunction()'><i class='fa fa-power-off fa-3x' aria-hidden='true'></i><div>";
		// }