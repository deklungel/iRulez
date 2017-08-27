<?PHP
if (mysqli_num_rows($qry2) != 0) {

										$sql_statement = "SELECT * FROM html_Radio_zenders where soort = 'fa-music'";
										$qry = $mysqli->query($sql_statement);
										$sql_statement = "SELECT * FROM html_Radio_zenders where soort = 'fa-youtube'";
										$qry3 = $mysqli->query($sql_statement);
										$sql_statement = "SELECT * FROM html_Radio_zenders where soort = 'fa-playlist'";
										$qry4 = $mysqli->query($sql_statement);

												
													while($radio = $qry2->fetch_assoc()) {		
														echo "<div class='volumerow row'>";
															echo '<div class="scrolling col-md-12 col-sm-12 col-xs-12 col-xxs-12 col-xxxs-12 col-xxxxs-12 ">';
															echo '<h3 id="marquee'.strtolower($radio['naam']).'" class="marquee'.strtolower($radio['naam']).'"></h3>';
															echo' </div>';
															
															echo '<div class="text-center col-xs-4 col-xxs-4 col-xxxs-12 col-xxxxs-12 col-xs-push-4 col-xxs-push-4 col-xxxs-push-0  col-xxxxs-push-0">';
															echo "<h2>Kodi ".$radio['omschrijving']."</h2>";
															echo '<i class="fa fa-music fa-2" aria-hidden="true"></i>';
															echo "<select id='radioUrl".strtolower($radio['naam'])."' onchange='publishRadio(\"".strtolower($radio['naam'])."\")'>";
																echo (" <option value='' >None</option>");
															if (mysqli_num_rows($qry) > 0)
															{
																echo '<optgroup label="Radio">';
															}
															while($row = $qry->fetch_assoc()) {
																echo (" <option value='".$row['url']."'>".ucfirst($row['naam'])."</option>");
															}
															if (mysqli_num_rows($qry3) > 0)
															{
																echo '<optgroup label="Youtube">';
															}
															while($row = $qry3->fetch_assoc()) {
																echo "<option value='".$row['url']."'>".ucfirst($row['naam'])."</option>";
															}
															if (mysqli_num_rows($qry4) > 0)
															{
																echo '<optgroup label="Playlist">';
															}
															while($row = $qry4->fetch_assoc()) {
																echo "<option value='".$row['url']."'>".ucfirst($row['naam'])."</option>";
															}
															echo '</select>';
															echo '<div class="youtube">';
															echo '<input type="url" placeholder="Youtube url" id="youtube'.strtolower($radio['naam']).'">';
															echo '<i id="youtube'.strtolower($radio['naam']).'"  class="fa fa-play fa-1" aria-hidden="true" onclick="clickyoutube(\''.strtolower($radio['naam']).'\')"></i></br>';
															echo '</div>';
															echo '</div>';
															
															echo '<div class="text-center col-xs-4 col-xxs-4 col-xxxs-12 col-xxxxs-12 col-xs-pull-4 col-xxs-pull-4 col-xxxs-pull-0 col-xxxxs-pull-0">';
															echo '<i disabled id="play'.strtolower($radio['naam']).'" class="fa fa-play fa-3" aria-hidden="true" onclick="clickPlay(\''.strtolower($radio['naam']).'\')"></i></br>';
															echo '<i id="pause'.strtolower($radio['naam']).'" class="fa fa-pause fa-3" aria-hidden="true" onclick="clickPause(\''.strtolower($radio['naam']).'\')"></i></br>';
															echo '<i id="stop'.strtolower($radio['naam']).'" class="fa fa-stop fa-3" aria-hidden="true" onclick="clickStop(\''.strtolower($radio['naam']).'\')"></i></br>';
															echo '<label class="Time'.strtolower($radio['naam']).'"></label>';
															echo '</div>';							
															
															echo '<div class="volume col-xs-4 col-xxs-4 col-xxxs-12 col-xxxxs-12">';
																	echo'<div class="volume_content"><div id="Volume-'.strtolower($radio['naam']).'"></div></div>';
																	echo "<p hidden class='radioId'>".strtolower($radio['naam'])."</p>";
															echo '</div>';
														
														echo' <script type="text/javascript">';
															echo' $(document).ready(function () {';
															echo'		$("#Volume-'.strtolower($radio['naam']).'").roundSlider({';
															echo'			value: 0,';
															echo'			sliderType: "min-range",';
															echo'			handleShape: "square",';
															echo'			circleShape: "pie",';
															echo'			editableTooltip: true,';
															echo'			min: "0",';
															echo'			max: "100",';
															echo'			startAngle: 315,';
															echo'			tooltipFormat: "changeTooltip",';
															echo'			drag: function(event) {';
															echo'				var value = event.value;';
															echo'				ChangeVolume(value,"'.strtolower($radio['naam']).'")';
															echo'			},';
															echo'			change: function(event) {';
															echo'				var value = event.value;';
															echo'				ChangeVolume(value,"'.strtolower($radio['naam']).'")';
															echo'			}';
															echo'		});';
															echo'	});';
															echo' </script>';
													echo "</div>";
													}
												
												
									}
									
?>