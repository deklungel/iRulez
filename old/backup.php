<?php
//Version 1.0
if(!empty($_POST["delete"]))
{
	unlink($_POST["file"]);;
}
if(!empty($_POST["create"]))
{
	$filename='iRulez_backup_'.date('Ymd_H').'h'.date('i').'.sql';

	$result=exec('mysqldump '.$config['db_name'].' --password='.$config['db_password'].' --user='.$config['db_user'].' --single-transaction >'.$config['websiteLocation'].'db_backup/'.$filename,$output);

	if(empty($output)){
		echo "Database backup ok!";
		echo $config['websiteLocation'];
	}
	else {
		echo (var_dump($output)) ;
	}
}
if(!empty($_POST["restore"]))
{
	
	$result=exec('mysql -u '.$config['db_user'].' -p'.$config['db_password'].' '.$config['db_name'].'  < '.$config['websiteLocation'].$_POST["file"],$output);

	if(empty($output)){
		echo "Database restore ok!";
	}
	else {
		echo (var_dump($output)) ;
	}
}

if(!empty($_POST["upload"]))
{
	// Check for errors
if($_FILES['file_upload']['error'] > 0){
    die('An error ocurred when uploading.');
}

// Check filetype
if($_FILES['file_upload']['type'] != 'application/octet-stream'){
    die('Unsupported filetype uploaded.');
}

// Check filesize
if($_FILES['file_upload']['size'] > 500000){
    die('File uploaded exceeds maximum upload size.');
}

// Check if the file exists
if(file_exists('db_backup/' . $_FILES['file_upload']['name'])){
    die('File with that name already exists.');
}

// Upload file
if(!move_uploaded_file($_FILES['file_upload']['tmp_name'], 'db_backup/' . $_FILES['file_upload']['name'])){
    die('Error uploading file - check destination is writeable.');
}

echo ('File uploaded successfully.');
	
}
//

$thelist='';

  if ($handle = opendir('./db_backup')) {
    while (false !== ($file = readdir($handle))) {
      if ($file != "." && $file != "..") {
        $thelist .= '
		<tr>
			<td><a href="db_backup/'.$file.'">'.$file.'</a></td>
			<td>
				<form method="post" action="?table=backup">
					<input type="hidden" name="file" value="db_backup/'.$file.'" />
					<input name="delete" type="submit" value="Delete" />
				</form>
			</td>
			<td>
				<form method="post" action="?table=backup">
					<input type="hidden" name="file" value="db_backup/'.$file.'" />
					<input name="restore" type="submit" value="Restore" />
				</form>
			</td>
		</tr>';
      }
    }
    closedir($handle);
  }
?>
<h1>Backups:</h1>
<table>
<?php echo $thelist; ?>
</table>
<h1>Create database backup</h1>
<form method="post" action="?table=backup">
					<input name="create" type="submit" value="Create Backup" />
</form><br>
<h1>Upload database file</h1>
<form action="?table=backup" method="post" enctype="multipart/form-data">
    <table>
	<tr><td>
	Select sql database file to upload:</td>
    <td><input type="file" name="file_upload" id="file_upload"></td></tr>
    <tr><td colspan='2'><input type="submit" value="Upload database File" name="upload"></td></tr>
	</table>
</form>
