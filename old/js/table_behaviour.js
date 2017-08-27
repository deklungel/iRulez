//Version 1.0
var datagrid = new DatabaseGrid();
window.onload = function() { 

	// key typed in the filter field
	$("#filter").keyup(function() {
		datagrid.EditableGrid.filter( $(this).val());

		// To filter on some columns, you can set an array of column index 
		//datagrid.EditableGrid.filter( $(this).val(), [0,3,5]);
	  });

	$("#showaddformbutton").click( function()  {
	  showAddForm();
	});
	$("#cancelbutton").click( function() {
	  showAddForm();
	});

	$("#addbutton").click(function() {
	  datagrid.addRow();
	});


}; 
