<?php
//Version 1.0
$service=$_GET["service"];
echo 'modules/'.$service.'.out.log';
//$data = file_get_contents('modules/Dummy/dummy.out.log');
$data = file_get_contents('modules/'.$service.'.out.log');
echo '<textarea id="textarea_id" style="width: 100%; height: 300px;">', htmlspecialchars($data), '</textarea>';
?>
<button onclick="myFunction()">Reload page</button>
<script src="js/jquery-2.2.3.min.js"></script>
<script>
function myFunction() {
    location.reload();
	var textarea = document.getElementById('textarea_id');
textarea.scrollTop = textarea.scrollHeight;
}
var textarea = document.getElementById('textarea_id');
textarea.scrollTop = textarea.scrollHeight;
</script>