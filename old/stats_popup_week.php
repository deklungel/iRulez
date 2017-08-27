<?php
//Version 1.0
if (isset($_POST['Generate']) || isset($_POST['Output'])){
	$week = explode("-", $_POST['Week']);
	if(isset($_POST['Output']) && $_POST['Output'] != ""){
		$query1 = "SELECT id_Core_Arduino_Output, SUM(time_delta) as time, weekday(Time_on) as day, Core_Arduino_Outputs.naam FROM Core_Stats INNER JOIN Core_Arduino_Outputs on Core_Stats.id_Core_Arduino_Output = Core_Arduino_Outputs.id WHERE id_Core_Arduino_Output = ".$_POST['Output']." AND YEAR(Time_on) = ".$week[1]." AND WEEK(Time_on,1) = ".$week[0]." GROUP BY id_Core_Arduino_Output, weekday(Time_on) ORDER BY time DESC";
		$query2 = "SELECT id_Core_Arduino_Output, time_delta as time, Time_on, Core_Arduino_Outputs.naam FROM Core_Stats INNER JOIN Core_Arduino_Outputs on Core_Stats.id_Core_Arduino_Output = Core_Arduino_Outputs.id WHERE id_Core_Arduino_Output = ".$_POST['Output']." AND YEAR(Time_on) = ".$week[1]." AND WEEK(Time_on,1) = ".$week[0]." ORDER BY time DESC";
	}
	else{
		$query1 = "SELECT id_Core_Arduino_Output, SUM(time_delta) as time, weekday(Time_on) as day, Core_Arduino_Outputs.naam FROM Core_Stats INNER JOIN Core_Arduino_Outputs on Core_Stats.id_Core_Arduino_Output = Core_Arduino_Outputs.id WHERE YEAR(Time_on) = ".$week[1]." AND WEEK(Time_on,1) = ".$week[0]." GROUP BY id_Core_Arduino_Output, weekday(Time_on) ORDER BY time DESC";
		$query2 = "SELECT id_Core_Arduino_Output, time_delta as time, Time_on, Core_Arduino_Outputs.naam FROM Core_Stats INNER JOIN Core_Arduino_Outputs on Core_Stats.id_Core_Arduino_Output = Core_Arduino_Outputs.id WHERE YEAR(Time_on) = ".$week[1]." AND WEEK(Time_on,1) = ".$week[0]." ORDER BY time DESC";
	}
	
	
	$data =array();
	$records = mysqli_query($mysqli,$query1);
		$counter = 0;
		while($record = mysqli_fetch_assoc($records)){
			$hour = round($record['time']/3600,0);
			if (empty($data[$record['naam']]))
			{
				for ($i = 0; $i <8; $i++){
					$data[$record['naam']][$i] = 0;
				}
				$counter++;
			}
			if($data[$record['naam']][$record['day']] + $hour > 24){
				$deltaDay =  floor($data[$record['naam']][$record['day']] + $hour / 24 );
				$j = 0;
				for ($i = $record['day']; $i < $record['day'] + $deltaDay; $i++){
					if (isset($data[$record['naam']][$i])) {  
					$data[$record['naam']][$i] = 24;
					$j = $i+1;
					}
				}
				if (isset($data[$record['naam']][$i])) {  
					$data[$record['naam']][$j] = $hour % 24;
				}
				
			}
			else{
				$data[$record['naam']][$record['day']]  = $hour ;
			}
			$data[$record['naam']][7]  = $data[$record['naam']][7] + $hour ;
			if($counter == 15){
				break;
			}
		}	
			if (empty($data)){
				for ($i = 0; $i <8; $i++){
					$data['no data'][$i] = 0;
				}
			}


	$dataTable =array();
	$records = mysqli_query($mysqli,$query2);
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
		
	function getWeekDates($year, $week)
	{
		$from = date("d/m", strtotime("{$year}-W{$week}-1")); //Returns the date of monday in week
		$to = date("d/m", strtotime("{$year}-W{$week}-7"));   //Returns the date of sunday in week
	 
		return 'Week '.$week.' ('.$from.' - '.$to.')';
	 
	}


}


?>
<html>

<head>
    <title>Statistics</title>
	<h1><?PHP echo getWeekDates($week[1],$week[0]); ?></h1>
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


<table>
<tr>
<td><button onclick="location.href = 'edit.php?table=statistics';">Back </button></td>
<td>
	<form action="edit.php?table=stats_popup_week" method="post">
	  <input type="hidden" name='Week' value='<?php echo $_POST['Week']; ?>'></input>
	  <select name="Output">
		<?php 
			$records = mysqli_query($mysqli,"SELECT DISTINCT id_Core_Arduino_Output, Core_Arduino_Outputs.naam FROM Core_Stats INNER JOIN Core_Arduino_Outputs on Core_Stats.id_Core_Arduino_Output = Core_Arduino_Outputs.id WHERE YEAR(Time_on) = ".$week[1]." AND WEEK(Time_on,1) = ".$week[0]." ORDER BY naam");
			while($record = mysqli_fetch_assoc($records)){
				echo '<option value="'.$record['id_Core_Arduino_Output'].'">'.$record['naam'].'</option>';
			}
		?>
		
	  </select>
	  <input name="Filter" type="submit" value="Filter">
	</form>
</td>
<td>
	<?PHP
		if(isset($_POST['Output'])&& $_POST['Output'] != ""){
			echo '<form action="edit.php?table=stats_popup_week" method="post">
				  <input type="hidden" name="Week" value='.$_POST['Week'].'></input>
				  <input type="hidden" name="Output" value=""></input>
				  <input name="Filter" type="submit" value="Clear">
				  </form>';
		}
	?>
</td>
</tr>
</table>

  



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
		echo("value: ".$record[7].", ");
		echo("label: \"".key($data)."\", ");
		echo("subData: [");
		for ($i = 0; $i <7; $i++){
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
        tooltipTemplate: '<%= value %>h',
		setBarValuesDecimals: 2
	    }
		
	var bardata = {
        labels: ["Mon", "Thu", "Wed", "Thur", "Fri", "Sat","Sun"],
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
