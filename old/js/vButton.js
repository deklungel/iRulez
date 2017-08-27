//Version 1.0
/**
 *  highlightRow and highlight are used to show a visual feedback. If the row has been successfully modified, it will be highlighted in green. Otherwise, in red
 */
function highlightRow(rowId, bgColor, after)
{
	var rowSelector = $("#" + rowId);
	rowSelector.css("background-color", bgColor);
	rowSelector.fadeTo("normal", 0.5, function() { 
		rowSelector.fadeTo("fast", 1, function() { 
			rowSelector.css("background-color", '');
		});
	});
}

function highlight(div_id, style) {
	highlightRow(div_id, style == "error" ? "#e5afaf" : style == "warning" ? "#ffcc00" : "#999999");
}

      
/**
   updateCellValue calls the PHP script that will update the database. 
 */
function updateCellValue(EditableGrid, rowIndex, columnIndex, oldValue, newValue, row, onResponse)
{      
	$.ajax({
		url: 'update.php',
		type: 'POST',
		dataType: "html",
	   		data: {
			tablename : EditableGrid.name,
			id: EditableGrid.getRowId(rowIndex), 
			newvalue: EditableGrid.getColumnType(columnIndex) == "boolean" ? (newValue ? 1 : 0) : newValue, 
			colname: EditableGrid.getColumnName(columnIndex),
			coltype: EditableGrid.getColumnType(columnIndex)			
		},
		success: function (response) 
		{ 
			// reset old value if failed then highlight row
			var success = onResponse ? onResponse(response) : (response == "ok" || !isNaN(parseInt(response))); // by default, a sucessfull reponse can be "ok" or a database id 
			if (!success) EditableGrid.setValueAt(rowIndex, columnIndex, oldValue);
		    highlight(row.id, success ? "ok" : "error"); 
		},
		error: function(XMLHttpRequest, textStatus, exception) { alert("Ajax failure\n" + errortext); },
		async: true
	});
   
}
   


function DatabaseGrid() 
{ 
	this.EditableGrid = new EditableGrid("html_vButton", {
		enableSort: true,
	    // define the number of row visible by page
      	pageSize: 50,
      // Once the table is displayed, we update the paginator state
        tableRendered:  function() {  updatePaginator(this); },
   	    tableLoaded: function() { datagrid.initializeGrid(this); },
		modelChanged: function(rowIndex, columnIndex, oldValue, newValue, row) {
   	    	updateCellValue(this, rowIndex, columnIndex, oldValue, newValue, row);
       	}
 	});
	this.fetchGrid(); 
	
}

DatabaseGrid.prototype.fetchGrid = function()  {
	// call a PHP script to get the data
	this.EditableGrid.loadJSON("loaddata_vbutton.php?db_tablename=html_vButton");
};

DatabaseGrid.prototype.initializeGrid = function(grid) {

  var self = this;

// render for the action column
	grid.setCellRenderer("action", new CellRenderer({ 
		render: function(cell, id) {                 
				cell.innerHTML+= "<i onclick=\"datagrid.deleteRow("+id+");\" class='fa fa-trash-o red' ></i>";
		}
	})); 
	grid.setCellRenderer("glyphicon", new CellRenderer({ 
		render: function(cell, value) { 
				cell.innerHTML = value ? "<i class='fa "+ value.toLowerCase() +"' ></i>" : ""; cell.style.textAlign = "center"; 
		}
		})); 
		

		
	grid.renderGrid("tablecontent", "iRulez");
};    

DatabaseGrid.prototype.deleteRow = function(id) 
{

  var self = this;
  if ( confirm(vButtons_delete.replace('$', id))  ) {

        $.ajax({
		url: 'delete.php',
		type: 'POST',
		dataType: "html",
		data: {
			tablename : self.EditableGrid.name,
			id: id 
		},
		success: function (response) 
		{ 
			if (response == "ok" )
		        self.EditableGrid.removeRow(id);
		},
		error: function(XMLHttpRequest, textStatus, exception) { alert("Ajax failure\n" + errortext); },
		async: true
	});

        
  }
			
}; 


DatabaseGrid.prototype.addRow = function(id) 
{

  var self = this;

        $.ajax({
		url: 'add_vbutton.php',
		type: 'POST',
		dataType: "html",
		data: {
			tablename : self.EditableGrid.name,
			naam:  $("#naam").val(),
			space:  $("#space").val(),
			soort:  $("#soort").val(),
			glyphicon:  $("#glyphicon").val(),
			vButton:  $("#vButton").val(),
			favoriet:  $("#favoriet").val()
			
		},
		success: function (response) 
		{ 
			if (response.trim() == "ok" ) {
   
                // hide form
				showAddForm();   
				$("#naam").val('');
				$("#space").val('');
				$("#soort").val('');
				$("#glyphicon").val('');
				$("#vButton").val('');
				$("#favoriet").val('');
                alert(vButtons_add);
                self.fetchGrid();
           	}
            else 
              alert(response);
		},
		error: function(XMLHttpRequest, textStatus, exception) { alert("Ajax failure\n" + errortext); },
		async: true
	});

        
			
}; 




function updatePaginator(grid, divId)
{
    divId = divId || "paginator";
	var paginator = $("#" + divId).empty();
	var nbPages = grid.getPageCount();

	// get interval
	var interval = grid.getSlidingPageInterval(20);
	if (interval == null) return;
	
	// get pages in interval (with links except for the current page)
	var pages = grid.getPagesInInterval(interval, function(pageIndex, isCurrent) {
		if (isCurrent) return "<span id='currentpageindex'>" + (pageIndex + 1)  +"</span>";
		return $("<a>").css("cursor", "pointer").html(pageIndex + 1).click(function(event) { grid.setPageIndex(parseInt($(this).html()) - 1); });
	});
		
	// "first" link
	var link = $("<a class='nobg'>").html("<i class='fa fa-fast-backward'></i>");
	if (!grid.canGoBack()) link.css({ opacity : 0.4, filter: "alpha(opacity=40)" });
	else link.css("cursor", "pointer").click(function(event) { grid.firstPage(); });
	paginator.append(link);

	// "prev" link
	link = $("<a class='nobg'>").html("<i class='fa fa-backward'></i>");
	if (!grid.canGoBack()) link.css({ opacity : 0.4, filter: "alpha(opacity=40)" });
	else link.css("cursor", "pointer").click(function(event) { grid.prevPage(); });
	paginator.append(link);

	// pages
	for (p = 0; p < pages.length; p++) paginator.append(pages[p]).append(" ");
	
	// "next" link
	link = $("<a class='nobg'>").html("<i class='fa fa-forward'>");
	if (!grid.canGoForward()) link.css({ opacity : 0.4, filter: "alpha(opacity=40)" });
	else link.css("cursor", "pointer").click(function(event) { grid.nextPage(); });
	paginator.append(link);

	// "last" link
	link = $("<a class='nobg'>").html("<i class='fa fa-fast-forward'>");
	if (!grid.canGoForward()) link.css({ opacity : 0.4, filter: "alpha(opacity=40)" });
	else link.css("cursor", "pointer").click(function(event) { grid.lastPage(); });
	paginator.append(link);
}; 


function showAddForm() {
  if ( $("#addform").is(':visible') ) 
      $("#addform").hide();
  else
      $("#addform").show();
}

$('select').change(function() {
 if ($(this).children('option:first-child').is(':selected')) {
   $(this).addClass('placeholder');
 } else {
  $(this).removeClass('placeholder');
 }
});
   




  



