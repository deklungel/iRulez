<!--Version 1.0-->
<?PHP
	$dataDay =array();
	$records = mysqli_query($mysqli,"SELECT id_Core_Arduino_Output, SUM(time_delta) as time, hour(Time_on) as hour, Core_Arduino_Outputs.naam FROM Core_Stats INNER JOIN Core_Arduino_Outputs on Core_Stats.id_Core_Arduino_Output = Core_Arduino_Outputs.id WHERE DATE(Time_on) = CURDATE() GROUP BY id_Core_Arduino_Output, hour(Time_on) ORDER BY time DESC");
		$counter = 0;
		while($record = mysqli_fetch_assoc($records)){
			$min = round($record['time']/60,2);
			if (empty($dataDay[$record['naam']]))
			{
				for ($i = 0; $i <25; $i++){
					$dataDay[$record['naam']][$i] = 0;
				}
				$counter++;
			}
			if($dataDay[$record['naam']][$record['hour']] + $min > 60){
				$deltaHour =  floor($dataDay[$record['naam']][$record['hour']] + $min / 60);
				$j = 0;
				for ($i = $record['hour']; $i < $record['hour'] + $deltaHour; $i++){
					if (isset($dataDay[$record['naam']][$i])) {  
					$dataDay[$record['naam']][$i] = 60;
					$j = $i+1;
					}
				}
				if (isset($dataDay[$record['naam']][$j])) {  
					$dataDay[$record['naam']][$j] = $min % 60;
				}
				
			}
			else{
				$dataDay[$record['naam']][$record['hour']]  = $min ;
			}
			$dataDay[$record['naam']][24]  = $dataDay[$record['naam']][24] + $min ;
			if($counter == 15){
				break;
			}
		}	
			if (empty($dataDay)){
				for ($i = 0; $i <25; $i++){
					$dataDay['no data'][$i] = 0;
				}
			}
	
	$dataWeek =array();
	$records = mysqli_query($mysqli,"SELECT id_Core_Arduino_Output, SUM(time_delta) as time, WEEKDAY(Time_on) as week, Core_Arduino_Outputs.naam FROM Core_Stats INNER JOIN Core_Arduino_Outputs on Core_Stats.id_Core_Arduino_Output = Core_Arduino_Outputs.id WHERE YEAR(Time_on) = YEAR(CURDATE()) AND WEEK(Time_on,1) = WEEK(CURDATE(),1) GROUP BY id_Core_Arduino_Output, WEEKDAY(Time_on) ORDER BY time DESC");
	$counter = 0;
		while($record = mysqli_fetch_assoc($records)){
			$hour = round($record['time']/3600,0);
			if (empty($dataWeek[$record['naam']]))
			{
				for ($i = 0; $i <8; $i++){
					$dataWeek[$record['naam']][$i] = 0;
				}
				$counter++;
			}
			if($dataWeek[$record['naam']][$record['week']] + $hour > 24){
				$deltaDay =  floor($dataWeek[$record['naam']][$record['week']] + $hour / 24 );
				$j = 0;
				for ($i = $record['week']; $i < $record['week'] + $deltaDay; $i++){
					if (isset($dataWeek[$record['naam']][$i])) {  
					$dataWeek[$record['naam']][$i] = 24;
					$j = $i+1;
					}
					
					
				}
					if (isset($dataWeek[$record['naam']][$j])) {  
					$dataWeek[$record['naam']][$j] = $hour % 24;
					}
				
			}
			else{
				$dataWeek[$record['naam']][$record['week']]  = $hour ;
			}
			$dataWeek[$record['naam']][7]  = $dataWeek[$record['naam']][7] + $hour ;
			if($counter == 15){
				break;
			}
		}	
		if (empty($dataWeek)){
				for ($i = 1; $i <8; $i++){
					$dataWeek['no data'][$i] = 0;
				}
		}
	
	$dataCurrentMonth =array();
	$records = mysqli_query($mysqli,"SELECT id_Core_Arduino_Output, SUM(time_delta) as time, day(Time_on) as day, Core_Arduino_Outputs.naam FROM Core_Stats INNER JOIN Core_Arduino_Outputs on Core_Stats.id_Core_Arduino_Output = Core_Arduino_Outputs.id WHERE YEAR(Time_on) = YEAR(CURDATE()) AND MONTH(Time_on) = MONTH(CURDATE()) GROUP BY id_Core_Arduino_Output, day(Time_on) ORDER BY time DESC");
	$counter = 0;
		while($record = mysqli_fetch_assoc($records)){
			$min = round($record['time']/60,0);
			if (empty($dataCurrentMonth[$record['naam']]))
			{
				for ($i = 1; $i <33; $i++){
					$dataCurrentMonth[$record['naam']][$i] = 0;
				}
				$counter++;
			}
			if($dataCurrentMonth[$record['naam']][$record['day']] + $min > 1440){
				$deltaDay =  floor($dataCurrentMonth[$record['naam']][$record['day']] + $min / 1440 );
				$j = 0;
				for ($i = $record['day']; $i < $record['day'] + $deltaDay; $i++){
					if (isset($dataCurrentMonth[$record['naam']][$i])) {  
					$dataCurrentMonth[$record['naam']][$i] = 60;
					$j = $i+1;
					}
				}
				if (isset($dataCurrentMonth[$record['naam']][$j])) {  
					$dataCurrentMonth[$record['naam']][$j] = $min % 60;
				}
				
			}
			else{
				$dataCurrentMonth[$record['naam']][$record['day']]  = $min ;
			}
			$dataCurrentMonth[$record['naam']][32]  = $dataCurrentMonth[$record['naam']][32] + $min ;
			if($counter == 15){
				break;
			}
		}	
		if (empty($dataCurrentMonth)){
				for ($i = 1; $i <33; $i++){
					$dataCurrentMonth['no data'][$i] = 0;
				}
		}
		
	
		
		$dataYear =array();
	$records = mysqli_query($mysqli,"SELECT id_Core_Arduino_Output, SUM(time_delta) as time, month(Time_on) as month, Core_Arduino_Outputs.naam FROM Core_Stats INNER JOIN Core_Arduino_Outputs on Core_Stats.id_Core_Arduino_Output = Core_Arduino_Outputs.id WHERE Time_on > DATE_SUB(CURDATE(), INTERVAL 1 YEAR) AND (MONTH(Time_on) != MONTH(CURRENT_DATE) OR YEAR(Time_on) = YEAR(CURRENT_DATE))  GROUP BY id_Core_Arduino_Output, month(Time_on) ORDER BY time DESC");
		$counter = 0;
		while($record = mysqli_fetch_assoc($records)){
			$min = round($record['time']/60,0);
			if (empty($dataYear[$record['naam']]))
			{
				for ($i = 1; $i <14; $i++){
					$dataYear[$record['naam']][$i] = 0;
				}
				$counter++;
			}
			if($dataYear[$record['naam']][$record['month']] + $min > 44640){
				$deltaDay =  floor($dataYear[$record['naam']][$record['month']] + $min / 44640 );
				$j = 0;
				for ($i = $record['month']; $i < $record['month'] + $deltaDay; $i++){
					if (isset($dataYear[$record['naam']][$i])) {  
					$dataYear[$record['naam']][$i] = 44640;
					$j = $i+1;
					}
				}
				if (isset($dataYear[$record['naam']][$j])) {  
					$dataYear[$record['naam']][$j] = $min % 44640;
				}
			}
			else{
				$dataYear[$record['naam']][$record['month']]  = $min ;
			}
			$dataYear[$record['naam']][13]  = $dataYear[$record['naam']][13] + $min ;
			if($counter == 15){
				break;
			}
		}	
			if (empty($dataYear)){
				for ($i = 1; $i <14; $i++){
					$dataYear['no data'][$i] = 0;
				}
			}
	?>	


<!doctype html>
<html>

<head>
    <title>Statistics</title>
    <script src="js/Chart.js"></script>
    <script src="js/jquery-2.2.3.min.js"></script>
	<script src="js/js-webshim/polyfiller.js"></script>
</head>

<body>
<h1><?php echo ucfirst($language['Statistics_Title']);?></h1>
<h2><?php echo ucfirst($language['Statistics_1']);?></h2>			
			<table class="stats">
			 <tr>
			 <td><canvas id="chartDay" width="300" height="300"></canvas></td>
			 <td><div id="js-legendDay" class="chart-legend"></div></td>
			 <td><canvas id="subchartDay" width="500" height="300"></canvas></td>
			 </tr>
			 </table>

<script>
	webshim.setOptions("forms-ext", {
	"date": {
		"startView": 2,
		"startValue": "<?PHP echo date("Y-m-d"); ?>",
		"openOnFocus": true
	}
});
webshims.polyfill('forms forms-ext');

</script>
<form method="POST" action="edit.php?table=stats_popup_day" >
<input id="datePicker" name="Date" type="date" value="<?PHP echo date("Y-m-d"); ?>" max="<?PHP echo date("Y-m-d"); ?>"/>
 <input type="submit" name="Generate" value="<?php echo ucfirst($language['Statistics_generate']);?>">
</form>

<h2><?php echo ucfirst($language['Statistics_2']);?></h2>
			<table class="stats">
			 <tr>
			 <td><canvas id="chartWeek" width="300" height="300"></canvas></td>
			 <td><div id="js-legendWeek" class="chart-legend"></div></td>
			 <td><canvas id="subchartWeek" width="500" height="300"></canvas></td>
			 </tr>
			 </table>
			 
<form method="POST" action="edit.php?table=stats_popup_week" >
	<select name="Week">
	<?PHP
	function getWeekDates($year, $week)
{
    $from = date("d/m", strtotime("{$year}-W{$week}-1")); //Returns the date of monday in week
    $to = date("d/m", strtotime("{$year}-W{$week}-7"));   //Returns the date of sunday in week
 
    return 'Week '.$week.' ('.$from.' - '.$to.')';
 
}
	
	for ($i = 0; $i <= 51; $i++) {
		echo '<option value="'.date("W-Y",strtotime("-".$i." week")).'">'.getWeekDates(date("Y",strtotime("-".$i." week")),date("W",strtotime("-".$i." week"))).'</option>';
	}
	?>
	 
	</select>
 <input type="submit" name="Generate" value="<?php echo ucfirst($language['Statistics_generate']);?>">
</form>



<h2><?php echo ucfirst($language['Statistics_3']);?></h2>
			<table class="stats">
			 <tr>
			 <td><canvas id="chartCurrentMonth" width="300" height="300"></canvas></td>
			 <td><div id="js-legendCurrentMonth" class="chart-legend"></div></td>
			 <td><canvas id="subchartCurrentMonth" width="500" height="300"></canvas></td>
			 </tr>
			 </table>
			 



<form method="POST" action="edit.php?table=stats_popup_month" >
	<select name="Month">
	<?PHP
	for ($i = 0; $i <= 11; $i++) {
		echo '<option value="'.date("m-Y",strtotime("first day of -".$i." month")).'">'.date("M-Y",strtotime("first day of -".$i." month")).'</option>';
	}
	?>
	 
	</select>
 <input type="submit" name="Generate" value="<?php echo ucfirst($language['Statistics_generate']);?>">
</form>

<h2><?php echo ucfirst($language['Statistics_4']);?></h2>
			<table class="stats">
			 <tr>
			 <td><canvas id="chartYear" width="300" height="300"></canvas></td>
			 <td><div id="js-legendYear" class="chart-legend"></div></td>
			 <td><canvas id="subchartYear" width="500" height="300"></canvas></td>
			 </tr>
			 </table>
    <script>

	var optionsPie = {
        tooltipEvents: ["mousemove"],
        showTooltips: true,
        tooltipTemplate: '<%= label %> - <%= value %>min - <%= Math.round(circumference / 6.283 * 100) %>%',
		legendTemplate : '<ul class="tc-chart-js-legend"><% for (var i=0; i<segments.length; i++){%><li><span style="background-color:<%=segments[i].fillColor%>"></span><%if(segments[i].label){%><%=segments[i].label%><%}%></li><%}%></ul>'
    }
        // pie
		

    var dataDay = [
	<?PHP
	while ($record = current($dataDay)) {
		echo ("{");
		echo("value: ".$record[24].", ");
		echo("label: \"".key($dataDay)."\", ");
		echo("subData: [");
		for ($i = 0; $i <24; $i++){
					echo $record[$i].",";
		}
		echo ("]},");
    next($dataDay);
	}
	?>
	]
	
	var dataWeek = [
	<?PHP
	while ($record = current($dataWeek)) {
		echo ("{");
		echo("value: ".$record[7].", ");
		echo("label: \"".key($dataWeek)."\", ");
		echo("subData: [");
		for ($i = 1; $i <7; $i++){
					echo $record[$i].",";
		}
		echo ("]},");
    next($dataWeek);
	}
	?>
	]
	
	var dataCurrentMonth = [
	<?PHP
	while ($record = current($dataCurrentMonth)) {
		echo ("{");
		echo("value: ".$record[32].", ");
		echo("label: \"".key($dataCurrentMonth)."\", ");
		echo("subData: [");
		for ($i = 1; $i <32; $i++){
					echo $record[$i].",";
		}
		echo ("]},");
    next($dataCurrentMonth);
	}
	?>
	]
	
	
	
	var dataYear = [
	<?PHP
	while ($record = current($dataYear)) {
		echo ("{");
		echo("value: ".$record[13].", ");
		echo("label: \"".key($dataYear)."\", ");
		echo("subData: [");
		for ($i = 1; $i <13; $i++){
					echo $record[$i].",";
		}
		echo ("]},");
    next($dataYear);
	}
	?>
	]
	

	

    var canvasDay = document.getElementById("chartDay");
    var ctxDay = canvasDay.getContext("2d");
    var myPieChartDay = new Chart(ctxDay).Pie(dataDay,optionsPie);
	document.getElementById("js-legendDay").innerHTML = myPieChartDay.generateLegend();
	
	var canvasWeek = document.getElementById("chartWeek");
    var ctxWeek = canvasWeek.getContext("2d");
    var myPieChartWeek = new Chart(ctxWeek).Pie(dataWeek,optionsPie);
	document.getElementById("js-legendWeek").innerHTML = myPieChartWeek.generateLegend();
	
	var canvasCurrentMonth = document.getElementById("chartCurrentMonth");
    var ctxCurrentMonth = canvasCurrentMonth.getContext("2d");
    var myPieChartCurrentMonth = new Chart(ctxCurrentMonth).Pie(dataCurrentMonth,optionsPie);
	document.getElementById("js-legendCurrentMonth").innerHTML = myPieChartCurrentMonth.generateLegend();
	
	
	var canvasYear = document.getElementById("chartYear");
    var ctxYear = canvasYear.getContext("2d");
    var myPieChartYear = new Chart(ctxYear).Pie(dataYear,optionsPie);
	document.getElementById("js-legendYear").innerHTML = myPieChartYear.generateLegend();

	var optionsBAR = {
        tooltipEvents: ["mousemove"],
        showTooltips: true,
        tooltipTemplate: '<%= value %>min',
		setBarValuesDecimals: 2
	    }
		
	var optionsBARHours = {
        tooltipEvents: ["mousemove"],
        showTooltips: true,
        tooltipTemplate: '<%= value %> h',
		setBarValuesDecimals: 2
	    }
	
    // bar using pie's sub data
    var bardataDay = {
        labels: ["0", "1", "2", "3", "4", "5", "6","7", "8", "9", "10", "11", "12", "13","14", "15", "16", "17", "18", "19", "20","21", "22", "23"],
        datasets: [{
            label: "My Second dataset",
            fillColor: "rgba(220,220,220,0.5)",
            strokeColor: "rgba(220,220,220,0.8)",
            highlightFill: "rgba(220,220,220,0.75)",
            highlightStroke: "rgba(220,220,220,1)",
            data: dataDay[0].subData.map(function (point, i) {
                var pointTotal = 0;
                dataDay.forEach(function (point) {
                    pointTotal += point.subData[i]
                })
                return pointTotal;
            })
        }]
    };
	
	var subcanvasDay = document.getElementById("subchartDay")
    var subctxDay = subcanvasDay.getContext("2d");
    var myBarChartDay = new Chart(subctxDay).Bar(bardataDay,optionsBAR);
	
	var bardataWeek = {
        labels: ["Mon", "Thu", "Wed", "Thur", "Fri", "Sat","Sun"],
        datasets: [{
            label: "My Second dataset",
            fillColor: "rgba(220,220,220,0.5)",
            strokeColor: "rgba(220,220,220,0.8)",
            highlightFill: "rgba(220,220,220,0.75)",
            highlightStroke: "rgba(220,220,220,1)",
            data: dataWeek[0].subData.map(function (point, i) {
                var pointTotal = 0;
                dataWeek.forEach(function (point) {
                    pointTotal += point.subData[i]
                })
                return pointTotal;
            })
        }]
    };

    var subcanvasWeek = document.getElementById("subchartWeek")
    var subctxWeek = subcanvasWeek.getContext("2d");
    var myBarChartWeek = new Chart(subctxWeek).Bar(bardataWeek,optionsBARHours);
	
	var bardataCurrentMonth = {
        labels: ["1", "2", "3", "4", "5", "6","7", "8", "9", "10", "11", "12", "13","14", "15", "16", "17", "18", "19", "20","21", "22", "23", "24", "25", "26", "27", "28","29", "30", "31"],
        datasets: [{
            label: "My Second dataset",
            fillColor: "rgba(220,220,220,0.5)",
            strokeColor: "rgba(220,220,220,0.8)",
            highlightFill: "rgba(220,220,220,0.75)",
            highlightStroke: "rgba(220,220,220,1)",
            data: dataCurrentMonth[0].subData.map(function (point, i) {
                var pointTotal = 0;
                dataCurrentMonth.forEach(function (point) {
                    pointTotal += point.subData[i]
                })
                return pointTotal;
            })
        }]
    };

    var subcanvasCurrentMonth = document.getElementById("subchartCurrentMonth")
    var subctxCurrentMonth = subcanvasCurrentMonth.getContext("2d");
    var myBarChartCurrentMonth = new Chart(subctxCurrentMonth).Bar(bardataCurrentMonth,optionsBAR);
	
	var bardataYear = {
        labels: ["1", "2", "3", "4", "5", "6","7", "8", "9", "10", "11", "12"],
        datasets: [{
            label: "My Second dataset",
            fillColor: "rgba(220,220,220,0.5)",
            strokeColor: "rgba(220,220,220,0.8)",
            highlightFill: "rgba(220,220,220,0.75)",
            highlightStroke: "rgba(220,220,220,1)",
            data: dataYear[0].subData.map(function (point, i) {
                var pointTotal = 0;
                dataYear.forEach(function (point) {
                    pointTotal += point.subData[i]
                })
                return pointTotal;
            })
        }]
    };

    var subcanvasYear = document.getElementById("subchartYear")
    var subctxYear = subcanvasYear.getContext("2d");
    var myBarChartYear = new Chart(subctxYear).Bar(bardataYear,optionsBAR);


    // connect them both
    canvasDay.onclick = function (evt) {
        var activeSector = myPieChartDay.getSegmentsAtEvent(evt);

        myBarChartDay.datasets[0].bars.forEach(function (bar, i) {
            var pointTotal = 0;
            dataDay.forEach(function (point, j) {
                if (activeSector.length === 0 || point.label === activeSector[0].label) pointTotal += dataDay[j].subData[i]
            })

            bar.value = pointTotal;
        });

        myBarChartDay.update();
    };
	
	canvasWeek.onclick = function (evt) {
        var activeSector = myPieChartWeek.getSegmentsAtEvent(evt);

        myBarChartWeek.datasets[0].bars.forEach(function (bar, i) {
            var pointTotal = 0;
            dataWeek.forEach(function (point, j) {
                if (activeSector.length === 0 || point.label === activeSector[0].label) pointTotal += dataWeek[j].subData[i]
            })

            bar.value = pointTotal;
        });

        myBarChartWeek.update();
    };
	
	canvasCurrentMonth.onclick = function (evt) {
        var activeSector = myPieChartCurrentMonth.getSegmentsAtEvent(evt);

        myBarChartCurrentMonth.datasets[0].bars.forEach(function (bar, i) {
            var pointTotal = 0;
            dataCurrentMonth.forEach(function (point, j) {
                if (activeSector.length === 0 || point.label === activeSector[0].label) pointTotal += dataCurrentMonth[j].subData[i]
            })

            bar.value = pointTotal;
        });

        myBarChartCurrentMonth.update();
    };
	
	
	canvasYear.onclick = function (evt) {
        var activeSector = myPieChartYear.getSegmentsAtEvent(evt);

        myBarChartYear.datasets[0].bars.forEach(function (bar, i) {
            var pointTotal = 0;
            dataYear.forEach(function (point, j) {
                if (activeSector.length === 0 || point.label === activeSector[0].label) pointTotal += dataYear[j].subData[i]
            })

            bar.value = pointTotal;
        });

        myBarChartYear.update();
    };
	</script>
</body>

</html>
