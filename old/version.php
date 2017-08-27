<?php
//Version 1.91
?>
<link rel="stylesheet" href="css/bootstrap.min.css" type="text/css" media="screen">
<script src="js/jquery-2.2.3.min.js" type="text/javascript"></script>
<script src="js/version.js" type="text/javascript"></script>




<?PHP
	
	$records = mysqli_query($mysqli,"SELECT * FROM html_versions");
	while($record = mysqli_fetch_assoc($records)){
		$pieces = explode("/",$record['filename']);
		$result[$pieces[0]][$pieces[sizeof($pieces)-2]][$pieces[sizeof($pieces)-1]] = $record['version'];
	}


   function getFileList($dir, $recurse=false, $depth=false)
  {
    // array to hold return value
    $retval = array();

    // add trailing slash if missing
    if(substr($dir, -1) != "/") $dir .= "/";

    // open pointer to directory and read list of files
    $d = @dir($dir) or die("getFileList: Failed opening directory $dir for reading");
    while(false !== ($entry = $d->read())) {
      // skip hidden files
      if($entry[0] == ".") continue;
      if(is_dir("$dir$entry")) {
        $retval[] = array(
          "name" => "$dir$entry/",
          "type" => filetype("$dir$entry"),
          "size" => 0,
          "lastmod" => filemtime("$dir$entry")
        );
       if($recurse && is_readable("$dir$entry/")) {
            if($depth === false) {
            $retval = array_merge($retval, getFileList("$dir$entry/", true));
          } elseif($depth > 0) {
            $retval = array_merge($retval, getFileList("$dir$entry/", true, $depth-1));
          }
        }
	  } elseif(is_readable("$dir$entry")) {
        $retval[] = array(
          "name" => "$dir$entry",
          "type" => mime_content_type("$dir$entry"),
          "size" => filesize("$dir$entry"),
          "lastmod" => filemtime("$dir$entry")
        );
      }
    }
    $d->close();
    return $retval;
  }
  $ignoreArrayDIR = array("mysql","pytz","paho","telepot","schedule","js-webshim","fonts","font-awesome-4.1.0","WebService");
  $ignoreArrayDIRString = "";
  foreach ($ignoreArrayDIR as $value){
	 $ignoreArrayDIRString = $ignoreArrayDIRString."\/".$value."\/|";
  }
  $ignoreArrayDIRString = substr($ignoreArrayDIRString, 0, -1);
  
  $ignoreArrayFILE = array("astral.py","config.php");
  $ignoreArrayFILEString = "";
  foreach ($ignoreArrayFILE as $value){
	 $ignoreArrayFILEString = $ignoreArrayFILEString."\/".$value."|";
  }
  $ignoreArrayFILEString = substr($ignoreArrayFILEString, 0, -1);

  
  $dirlist = getFileList("/var/www/",true,3);
  
  foreach($dirlist as $file) {
     if((!preg_match("/\.php$|\.py$|\.css$|\.js$/", $file['name']) && $file['type'] != "dir") || preg_match("/".$ignoreArrayDIRString."/", $file['name']) || preg_match("/".$ignoreArrayFILEString."/", $file['name'])) continue;
		
			$split = explode("/", $file['name']);
			if($file['type'] != "dir"){
	
			$files = fopen($file['name'], "r") or die("Unable to open file!");
			//$version = fgets($files);
			//fclose($files);
			
			$f = fopen($file['name'], "r");
			// Read line by line until end of file
			$counter = 0;
			while(!feof($f)) { 
				$version = fgets($f);
				$counter++;
				if($counter == 2 || strpos($version,"Version")){
					break;
				}
			}

			
			
			$version = str_replace("<!--","",$version);
			$version = str_replace("-->","",$version);
			
			$version = str_replace("#","",$version);
			
			$version = str_replace("//","",$version);
			
			$version = str_replace("/*","",$version);
			$version = str_replace("*/","",$version);
			
			if(strpos($version, 'Version') === false)
			{
				$version = "Unknown";
			}
			else{
				$version = str_replace("Version","",$version);
			}

				if(preg_match("/\/modules\/.+/", $file['name'])){
					$ServerVersion = isset($result['Modules'][$split[sizeof($split)-2]][$split[sizeof($split)-1]]) ? trim($result['Modules'][$split[sizeof($split)-2]][$split[sizeof($split)-1]]) : 'Unknown';
					$dirArray['Modules'][$split[sizeof($split)-2]][] = array($split[sizeof($split)-1],trim($version),trim($ServerVersion));
					if (trim($version) <> trim($ServerVersion) && trim($ServerVersion != "Unknown")){
						$UpdateAll['Modules'][$split[sizeof($split)-2]][] = $split[sizeof($split)-1];
					}
					ksort($dirArray['Modules']);
					sort($dirArray['Modules'][$split[sizeof($split)-2]]);
				}
				else{
					$ServerVersion = isset($result['Website'][$split[sizeof($split)-2]][$split[sizeof($split)-1]]) ? trim($result['Website'][$split[sizeof($split)-2]][$split[sizeof($split)-1]]) : 'Unknown';
					$dirArray['Website'][$split[sizeof($split)-2]][] = array($split[sizeof($split)-1],trim($version),(isset($result['Website'][$split[sizeof($split)-2]][$split[sizeof($split)-1]]) ? trim($result['Website'][$split[sizeof($split)-2]][$split[sizeof($split)-1]]) : 'Unknown'));
					if (trim($version) <> trim($ServerVersion) && trim($ServerVersion != "Unknown")){
						$UpdateAll['Website'][$split[sizeof($split)-2]][] = $split[sizeof($split)-1];
					}
					ksort($dirArray['Website']);
					sort($dirArray['Website'][$split[sizeof($split)-2]]);
				}
				
			}	
		}
		ksort($dirArray);

		if(isset($result)){
			while ($NewFiles = current($result)) {
				while ($NewFiles2 = current($NewFiles)) {
						while ($NewFiles3 = current($NewFiles2)) {
							$new = true;
							if(isset($dirArray[key($result)][key($NewFiles)])){
								for ($i = 0; $i <sizeof($dirArray[key($result)][key($NewFiles)]); $i++){
									if($dirArray[key($result)][key($NewFiles)][$i][0] == key($NewFiles2)){
										$new = false;
									}
								}
							}
							if($new){
								$dirArray[key($result)][key($NewFiles)][] = array(key($NewFiles2),"New",$NewFiles3);
							}
						next($NewFiles2);	
						}
						
					
					next($NewFiles);
				}
				next($result);
			}
		}
?>
<h1>Versions</h1>
<form action="updateVersionDB.php">
<button>Sync</button>
</form>
<form action="updateSoftware.php" method="post">
<table class="table table-bordered">
<?PHP
	 $counter = 0;
	 while ($record = current($dirArray)) {
		echo '<tr class="level_0 collapsed" id="'.$counter.'" ><td colspan="4">'.key($dirArray).'</td></tr>';
		$parent = $counter;
		while ($record2 = current($record)) {
				$value = "";
			if(isset($UpdateAll[key($dirArray)][key($record)])){
				for ($i = 0; $i <sizeof($UpdateAll[key($dirArray)][key($record)]); $i++){
					if (key($dirArray) == "Modules") {
							$value .= "html/".strtolower(key($dirArray)).'/';
					}
					if(key($record) != "html" && key($dirArray) != "Modules"){
								$value .= "html/";
					}
					 $value .=  key($record).'/'.$UpdateAll[key($dirArray)][key($record)][$i].'|';
					}
					$value= substr($value, 0, -1);
			}
			echo '<tr class="level_1 parent_'.$parent.' collapsed" id="'.($counter+1).'" style="display: none;"><td '.(isset($UpdateAll[key($dirArray)][key($record)]) ? " colspan='3'>".key($record).'</td><td id="tdButton"><button type="submit" name="updateAll" value="'.$value.'" >Update</button></td>' : "colspan='4'>".key($record).'</td>').'</tr>';
			$counter ++;
			$subparrent = $counter;
			for ($i = 0; $i <sizeof($record2); $i++){
					echo '<tr class="level_2 parent_'.$subparrent.' collapsed" id="'.($counter+1).'" style="display: none;"><td>'.$record2[$i][0].'</td><td>'.$record2[$i][1].'</td><td>'.$record2[$i][2].'</td><td id="tdButton">';
					if ($record2[$i][2] <> $record2[$i][1] && $record2[$i][2] != "Unknown" ){
						echo '<button type="submit" name="update" value="';
						if (key($dirArray) == "Modules") {
							echo "html/".strtolower(key($dirArray)).'/';
						}
						if(key($record) != "html" && key($dirArray) != "Modules"){
							echo "html/";
						}
						echo key($record).'/'.$record2[$i][0].'">Update</button>';
					}
					echo '</td></tr>';
					$counter ++;
			}
			next($record);
		}
    next($dirArray);
	}
?>
</table>
</form>

