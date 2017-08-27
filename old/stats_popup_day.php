<?php
//Version 1.0
if (isset($_POST['Generate'])){
	$data =array();
		$records = mysqli_query($mysqli,"SELECT id_Core_Arduino_Output, time_delta as time, Time_on,Time_off, Core_Arduino_Outputs.naam FROM Core_Stats INNER JOIN Core_Arduino_Outputs on Core_Stats.id_Core_Arduino_Output = Core_Arduino_Outputs.id WHERE DatesON LIKE  '%".$_POST['Date']."%' ORDER BY time DESC");
		while($record = mysqli_fetch_assoc($records)){
			$dateON = new DateTime($record['Time_on']);
			if($record['Time_off'] != null){
				$dateOFF = new DateTime($record['Time_off']);
			}
			else{
				$dateOFF = new DateTime(date('Y-m-d H:i:s'));
			}
			$dateONToday = new DateTime(date("m/d/Y H:i:s",strtotime("midnight")));
			$now = strtotime(date('Y-m-d H:i:s'));
			$PostDate = new DateTime(date($_POST['Date']));
			if($dateON->format('d') != $dateONToday->format('d') && $dateON->format('m') == $dateONToday->format('m') && $record['time'] == null){
				$min = round(($now - strtotime("midnight"))/60,2) ;
				if($dateOFF->format('d') != $PostDate->format('d') && $dateOFF->format('m') == $PostDate->format('m'))
				{
					$min = 60 * 24;
				}
				else{
					$dateON = $dateONToday;
				}
			}
			elseif($dateON->format('d') != $dateONToday->format('d') && $record['time'] != null){
				$min = round((strtotime($record['Time_off']) - strtotime("midnight"))/60,2) ;
				$dateON = $dateONToday;	
			}
			elseif ($dateON->format('d') == $dateONToday->format('d') && $record['time'] == null)
			{
				$timeSecond = strtotime($record['Time_on']);
				$min = round(($now - $timeSecond)/60,2) ;
			}
			else{
				$min = round($record['time']/60,2);
			}
			
			
			if (empty($data[$record['naam']]))
			{
				for ($i = 0; $i <25; $i++){
					$data[$record['naam']][$i] = 0;
				}
			}
			
			
			$hour = $dateON->format('H');
			if ($hour == '00'){
				$hour = 0;
			}
			else{
				$hour = ltrim($hour, '0');
			}
			
			if($data[$record['naam']][$hour] + $dateON->format('i') + $min > 60){
				$data[$record['naam']][$hour]+= 60 - $dateON->format('i') ;
				$deltaHour =  floor(($min + $dateON->format('i'))/ 60);
				$j = $hour +1;
				for ($i = $hour +1; $i < $hour + $deltaHour; $i++){
					if (isset($data[$record['naam']][$i])) {  
					$data[$record['naam']][$i] = 60;
					$j = $i+1;
					}
				}
				if (isset($data[$record['naam']][$j])) {  
					$data[$record['naam']][$j] += ($min + $dateON->format('i')) % 60;

				}
				
			}
			else{
				$data[$record['naam']][$hour]+= $min ;
			}
			
			
			
			$data[$record['naam']][24]  += round($min,0) ;
		}	
	
	if (empty($data)){
				for ($i = 0; $i <25; $i++){
					$data['no data'][$i] = 0;
				}
			}
	
	
	$dataTable =array();
	$records = mysqli_query($mysqli,"SELECT id_Core_Arduino_Output, time_delta as time, DATE_FORMAT(Time_on,'%T') as TimeON,Time_on, DATE_FORMAT(Time_off,'%T') as TimeOFF, Core_Arduino_Outputs.naam FROM Core_Stats INNER JOIN Core_Arduino_Outputs on Core_Stats.id_Core_Arduino_Output = Core_Arduino_Outputs.id wHERE DatesON LIKE  '%".$_POST['Date']."%' ORDER BY time DESC");
		while($record = mysqli_fetch_assoc($records)){
			$timeOFF = $record['TimeOFF'];
			$timeON = $record['TimeON'];
			$time = $record['time'];
			if($timeOFF == null){
				$timeOFF = "ON";
				$datetimeON = new DateTime($timeON);
				if($datetimeON->format('d') != $dateONToday->format('d') && $datetimeON->format('m') == $dateONToday->format('m')){
					$time = $now - $dateONToday;
					$timeON = $record['Time_on'];
				}
				else{
					$timeSecond = strtotime($record['Time_on']);
					$time = round(($now - $timeSecond)/60,2) ;
				}
				
			}
			$hours = floor($time / 3600);
			$minutes = floor(($time / 60) % 60);
			$seconds = $time % 60;		
			
			
			$dataTable[]  = "<tr><td>".$record['naam']."</td><td>".$timeON."</td><td>".$timeOFF."</td><td>".$hours."</td><td>".$minutes."</td><td>".$seconds."</td></tr>";
			}
}
?>
<html>

<head>
    <title>Statistics</title>
	<h2><?PHP echo $_POST['Date'] ?></h2>
    <script src="js/Chart.js"></script>
    <script src="js/jquery-2.2.3.min.js"></script>
	<script src="js/js-webshim/polyfiller.js"></script>

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
<tr><th>Relais name</th><th>Time on</th><th>Time off</th><th>Duration (h)</th><th>Duration (min)</th><th>Duration (sec)</th></tr>
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
		echo("value: ".$record[24].", ");
		echo("label: \"".key($data)."\", ");
		echo("subData: [");
		for ($i = 0; $i <24; $i++){
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
        labels: ["0", "1", "2", "3", "4", "5", "6","7", "8", "9", "10", "11", "12", "13","14", "15", "16", "17", "18", "19", "20","21", "22", "23"],
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
