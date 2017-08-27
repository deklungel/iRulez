<?php
//Version 1.0 
if (isset($_POST['Generate'])){
	$month = explode("-", $_POST['Month']);
	$data =array();
	$records = mysqli_query($mysqli,"SELECT id_Core_Arduino_Output, SUM(time_delta) as time, day(Time_on) as day, Core_Arduino_Outputs.naam FROM Core_Stats INNER JOIN Core_Arduino_Outputs on Core_Stats.id_Core_Arduino_Output = Core_Arduino_Outputs.id WHERE YEAR(Time_on) = ".$month[1]." AND MONTH(Time_on) = ".$month[0]." GROUP BY id_Core_Arduino_Output, day(Time_on) ORDER BY time DESC");
		$counter = 0;
		while($record = mysqli_fetch_assoc($records)){
			$min = round($record['time']/60,0);
			if (empty($data[$record['naam']]))
			{
				for ($i = 1; $i <33; $i++){
					$data[$record['naam']][$i] = 0;
				}
				$counter++;
			}
			if($data[$record['naam']][$record['day']] + $min > 720){
				$deltaDay =  floor($data[$record['naam']][$record['day']] + $min / 720 );
				$j = 0;
				for ($i = $record['day']; $i < $record['day'] + $deltaDay; $i++){
					if (isset($data[$record['naam']][$i])) {  
					$data[$record['naam']][$i] = 60;
					$j = $i+1;
					}
				}
				if (isset($data[$record['naam']][$i])) {  
					$data[$record['naam']][$j] = $min % 60;
				}
				
			}
			else{
				$data[$record['naam']][$record['day']]  = $min ;
			}
			$data[$record['naam']][32]  = $data[$record['naam']][32] + $min ;
			if($counter == 15){
				break;
			}
		}	
			if (empty($data)){
				for ($i = 0; $i <33; $i++){
					$data['no data'][$i] = 0;
				}
			}


	$dataTable =array();
	$records = mysqli_query($mysqli,"SELECT id_Core_Arduino_Output, time_delta as time, Time_on, Core_Arduino_Outputs.naam FROM Core_Stats INNER JOIN Core_Arduino_Outputs on Core_Stats.id_Core_Arduino_Output = Core_Arduino_Outputs.id WHERE YEAR(Time_on) = ".$month[1]." AND MONTH(Time_on) = ".$month[0]." ORDER BY time DESC");
		while($record = mysqli_fetch_assoc($records)){
			$hours = floor($record['time'] / 3600);
			$minutes = floor(($record['time'] / 60) % 60);
			$seconds = $record['time'] % 60;
			
			$dateinsec=strtotime($record['Time_on']);
			$timeOff=$dateinsec+$record['time'];
			if($hours >0 or $minutes > 0 or $seconds > 0){
				$dataTable[]  = "<tr><td>".$record['naam']."</td><td>".date('d-m-y',$dateinsec)."</td><td>".date('H:i:s',$dateinsec)."</td><td>".date('d-m-y',$timeOff)."</td><td>".date('H:i:s',$timeOff)."</td><td>".$hours."</td><td>".$minutes."</td><td>".$seconds."</td></tr>";
			
			}
		}
}
?>
<html>

<head>
    <title>Statistics</title>
	<h2></h2>
    <script src="js/Chart.js"></script>
    <script src="js/jquery-2.2.3.min.js"></script>

</head>
<table class="stats">
			 <tr>
			 <td><canvas id="chart" width="300" height="300"></canvas></td>
			 <td><div id="js-legend" class="chart-legend"></div></td>
			 <td><canvas id="subchart" width="500" height="300"></canvas></td>
			 </tr>
</table>

<button onclick="history.go(-1);">Back </button>


<table class="statsTable" align="center">
<tr><th>Relais name</th><th colspan="2">Time on</th><th colspan="2">Time off</th><th>Duration (h)</th><th>Duration (min)</th><th>Duration (sec)</th></tr>
<?PHP
foreach ($dataTable as $line) {
    echo $line;
}
?>
</table>

<script>

	var optionsPie = {
        tooltipEvents: ["mousemove"],
        showTooltips: true,
        tooltipTemplate: '<%= label %> - <%= value %>min - <%= Math.round(circumference / 6.283 * 100) %>%',
		legendTemplate : '<ul class="tc-chart-js-legend"><% for (var i=0; i<segments.length; i++){%><li><span style="background-color:<%=segments[i].fillColor%>"></span><%if(segments[i].label){%><%=segments[i].label%><%}%></li><%}%></ul>'
    }
        // pie
		

    var data = [
	<?PHP
	while ($record = current($data)) {
		echo ("{");
		echo("value: ".$record[32].", ");
		echo("label: \"".key($data)."\", ");
		echo("subData: [");
		for ($i = 1; $i <32; $i++){
					echo $record[$i].",";
		}
		echo ("]},");
    next($data);
	}
	?>
	]
	
	var canvas = document.getElementById("chart");
    var ctx = canvas.getContext("2d");
    var myPieChart = new Chart(ctx).Pie(data,optionsPie);
	document.getElementById("js-legend").innerHTML = myPieChart.generateLegend();	
	
	var optionsBAR = {
        tooltipEvents: ["mousemove"],
        showTooltips: true,
        tooltipTemplate: '<%= value %>min',
		setBarValuesDecimals: 2
	    }
		
	var bardata = {
        labels: ["1", "2", "3", "4", "5", "6","7", "8", "9", "10", "11", "12", "13","14", "15", "16", "17", "18", "19", "20","21", "22", "23", "24", "25", "26", "27", "28","29", "30", "31"],
        datasets: [{
            label: "My Second dataset",
            fillColor: "rgba(220,220,220,0.5)",
            strokeColor: "rgba(220,220,220,0.8)",
            highlightFill: "rgba(220,220,220,0.75)",
            highlightStroke: "rgba(220,220,220,1)",
            data: data[0].subData.map(function (point, i) {
                var pointTotal = 0;
                data.forEach(function (point) {
                    pointTotal += point.subData[i]
                })
                return pointTotal;
            })
        }]
    };
	
	var subcanvas = document.getElementById("subchart")
    var subctx = subcanvas.getContext("2d");
    var myBarChart = new Chart(subctx).Bar(bardata,optionsBAR);
	
	
	// connect them both
    canvas.onclick = function (evt) {
        var activeSector = myPieChart.getSegmentsAtEvent(evt);

        myBarChart.datasets[0].bars.forEach(function (bar, i) {
            var pointTotal = 0;
            data.forEach(function (point, j) {
                if (activeSector.length === 0 || point.label === activeSector[0].label) pointTotal += data[j].subData[i]
            })

            bar.value = pointTotal;
        });

        myBarChart.update();
    };
	
	</script>
</body>

</html>
