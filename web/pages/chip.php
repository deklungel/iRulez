<html>
<head>
	<title>Demo reading data from Mysql</title>
	
	<link rel="stylesheet" type="text/css" href="/css/irulez.css">
	<script
  src="https://code.jquery.com/jquery-3.2.1.js"
  integrity="sha256-DZAnKJ/6XZ9si04Hgrsxu/8s717jcIzLy3oi35EouyE="
  crossorigin="anonymous"></script>
	<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/snap.svg/0.5.1/snap.svg-min.js"></script>
	<script type="text/Javascript" src="/js/iRulez.js"></script>
	<script type="text/javascript">
	var _prongs = [];
	var _prongAmount = 16;
	var _currentprong = 0;
	var toggleer;

	$(document).ready(function()
	{
		$(".sendState").click(function()
		{
			console.log("Mac:" + $(".chippiemac").val());
			console.log("Sending new state: H: " + $(this).data("H") + " L: " + $(this).data("L"));
			iRulez.Data.triggerDeviceState($(".chippiemac").val(),
											$(this).data("H"),
											$(this).data("L"),
											function(success)
											{
												if(success)
												{
													alert("Success");
												}
												else
												{
													alert("fail");
												}
											});
		});
		
		refreshDeviceStatus(10);
		
		var s = Snap("#chip");
		var chip_center = s.rect(25,15,245,80,10,0);
		for(var v=1;v<=_prongAmount/2;v++)
		{
			var circle = s.circle(((10*v) + (23*v)),15,10);
			circle.attr({
				fill: "#FFD700",
				stroke: "",
				strokeWidth: 0,
				id: _prongs.length
			});
			circle.click(function(e)
			{
				activateProng(e.toElement.id);
			});
			circle.status = 0;
			_prongs.push(circle);
		}
		for(var v=1;v<=_prongAmount/2;v++)
		{
			var circle = s.circle(((10*v) + (23*v)),95,10);
			circle.attr({
				fill: "#FFD700",
				stroke: "",
				strokeWidth: 0,
				id: _prongs.length
			});
			circle.click(function(e)
			{
				activateProng(e.toElement.id);
			});
			circle.status = 0;
			_prongs.push(circle);
		}
		
		// Events	
		$(".Toggle").click(function()
		{
			if($(this).data("status") == "off")
			{
				$(this).data("status", "on");
				startToggling();
				
			}
			else
			{
				$(this).data("status", "off");
				stopToggling();
			}
		});
	});

	function activateProng(index)
	{
		index = parseInt(index);
		// first time, they're down
		if(_prongs[index].status == 'undefined') _prongs[index].status = 0;
		_prongs[index].status += 1;
		if(_prongs[index].status > 2) _prongs[index].status = 0;
		showDeviceState();
			
		if(_prongs[index].status == 0)
		{
			_prongs[index].attr({
				fill: "#FFD700",
				stroke: "#000",
				strokeWidth:0
			});
		}
		else if(_prongs[index].status == 1)
		{
			_prongs[index].attr({
				fill: "#bada55",
				stroke: "#000",
				strokeWidth: 5
			});
		}
		else
		{
			_prongs[index].attr({
				fill: "red",
				stroke: "#000",
				strokeWidth: 5
			});
		}
	
	}

	function startToggling()
	{
		_prongs[_currentprong].attr({
			fill: "#bada55",
			stroke: "#000",
			strokeWidth: 5
		});
		toggleer = setInterval(function(){
			_prongs[_currentprong].attr({
				fill: "#FFD700",
				stroke: "",
				strokeWidth: 0
			});
			_prongs[_currentprong].status = 0;
			if(_currentprong>=_prongAmount-1) _currentprong = 0;
			else _currentprong += 1;
			activateProng(_currentprong);
		}, 500);
	}
	function stopToggling()
	{
		_prongs[_currentprong].attr({
			fill: "#FFD700",
			stroke: "#000",
			strokeWidth:0
		});
		clearInterval(toggleer);
	}
	function showDeviceState()
	{
		var _stateH = "";
		var _stateL = "";
		for(var v=0;v<_prongs.length;v++)
		{
			if(_prongs[v].status > 1)
			{
				_stateL += "1";
				_stateH += "0";
			}
			else if(_prongs[v].status == 1)
			{
				_stateL += "0";
				_stateH += "1";
			}
			else
			{
				_stateL += "0";
				_stateH += "0";
			}
		}
		$(".sendState").data("H", _stateH);
		$(".sendState").data("L", _stateH);
		$(".sendState").data("HexH", getHEXString(_stateH));
		$(".sendState").data("HexL", getHEXString(_stateL));
		
		var _result = "<b>bit</b><br />H : " + _stateH + " L: " + _stateL + "<br /><b>Hex</b><br />H : " + getHEXString(_stateH) + " L: " + getHEXString(_stateL);
		$(".deviceState").html(_result);
	}
	function getHEXString(substring)
	{
		var hexValue = parseInt(substring, 2).toString(16);
		if(hexValue.length == 1) hexValue = '0'+hexValue
		return hexValue;
	}
	var _currentSecond = 0;
	function refreshDeviceStatus(intervalSeconds)
	{
		_currentSecond = intervalSeconds;
		setInterval(function()
		{
			if(_currentSecond<=0 || _currentSecond == intervalSeconds)
			{
				_currentSecond = intervalSeconds;
				iRulez.Data.getDevice($(".chippiemac").val(), function(data)
				{
					var _details = "id: " + data.id
							+"<br />Naam: " + data.Naam
							+ "<br />Created: "+ data.Created 
							+ "<br />LastModified: " + data.LastModified
							+ "<br />Mac: " + data.MAC
							+ "<br />State: " + data.State + "<br /><label class=refresh></label>";
					
					$(".deviceDetails").html(_details);
				});
			}
			_currentSecond-=1;
			$(".deviceDetails .refresh").html("Refresh in " + (_currentSecond +1));
			
		}, 1000);
	}
	</script>	
  </head>
<body>
<h1>Chippie</h1>
<input type="hidden" value="<?php echo $_GET['MAC'] ?>" class="chippiemac"/>
<button class="Toggle" data-status="off">Start/stop toggle</button>
<div class="deviceDetails" style="float:right"></div>
<br />
<svg id="chip" />

<div class="deviceState">
</div>
<button class="sendState">Send new state to API</button>
</body>
</html>