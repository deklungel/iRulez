//Version 1.0
function selectall(cls)
{
	var splitCls = cls.split("|");
	for(i = 0; i < splitCls.length; i++){
		var lst = document.getElementsByName(splitCls[i]);
		for (var j = 0; j < lst.length; j++){
			var nodes = document.getElementsByName(splitCls[i])[j].childNodes;	
			for(var i=0; i<nodes.length; i++) {
				 nodes[i].selected = true;
			 }
		}
	}
}
function unselectall(cls)
{
	var splitCls = cls.split("|");
	for(i = 0; i < splitCls.length; i++){
		var lst = document.getElementsByName(splitCls[i]);
		for (var j = 0; j < lst.length; j++){
			var nodes = document.getElementsByName(splitCls[i])[j].childNodes;	
			for(var i=0; i<nodes.length; i++) {
				 nodes[i].selected = false;
			 }
		}
	}
}
function OnChangeCheckbox (checkbox,cls) {
		if (checkbox.checked) {
			show(cls);
		}
		else {
			hide(cls);
		}
}
function hide(cls) {
	var splitCls = cls.split("|");
	for(i = 0; i < splitCls.length; i++){
		var lst = document.getElementsByClassName(splitCls[i]);
		for (var j = 0; j < lst.length; j++){
			lst[j].style.display = 'none';
		}
	}
}
function show(cls) {
	var splitCls = cls.split("|");
	for(i = 0; i < splitCls.length; i++){
		var lst = document.getElementsByClassName(splitCls[i]);
		for (var j = 0; j < lst.length; j++){
			lst[j].style.display = '';
		}
	}
}