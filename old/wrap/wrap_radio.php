<?php
//Version 1.1
?>
<div id="wrap">
		<h1><?PHP echo ucfirst($language['Title_Radio']); ?></h1> 

	<!-- Feedback message zone -->
	<div id="message"></div>

	<div id="toolbar">
	  <input type="text" id="filter" name="filter" placeholder="<?php echo ucfirst($language['lable_filter']); ?>"  />
	</div>
	<!-- Grid contents -->
	<div id="tablecontent"></div>

	<!-- Paginator control -->
	<div id="paginator"></div>
</div>

<script src="js/editablegrid-2.1.0-b25.js"></script>   
<script src="js/jquery-2.2.3.min.js" ></script>
<!-- EditableGrid test if jQuery UI is present. If present, a datepicker is automatically used for date type -->
<script src="//ajax.googleapis.com/ajax/libs/jqueryui/1.10.4/jquery-ui.min.js"></script>

