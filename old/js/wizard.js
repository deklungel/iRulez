//Version 1.1
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
function enable(cls) {
	var splitCls = cls.split("|");
	for(i = 0; i < splitCls.length; i++){
		var lst = document.getElementsByName(splitCls[i]);
		for (var j = 0; j < lst.length; j++){
			lst[j].disabled = false;
		}
	}
}
function checkEnableDisable(cls,force) {
	var splitCls = cls.split("|");
	for(i = 0; i < splitCls.length; i++){
		var splitCls2 = splitCls[i].split(";");
		var lst = document.getElementsByName(splitCls2[1]);
		var x = document.getElementById(splitCls2[0]).checked;
		for (var j = 0; j < lst.length; j++){
			if(x == true || force == "BD"){
				lst[j].disabled = false;
				document.getElementById(splitCls2[0]).checked = true;
			}
			else{
				lst[j].disabled = true;
				document.getElementById(splitCls2[0]).checked = false;
			}
		}
	}
}

function EnableID(cls) {
	var splitCls = cls.split("|");
	for(i = 0; i < splitCls.length; i++){
		document.getElementById(splitCls[i]).disabled = false;
	}
}

function disable(cls) {
	var splitCls = cls.split("|");
	for(i = 0; i < splitCls.length; i++){
		var lst = document.getElementsByName(splitCls[i]);
		for (var j = 0; j < lst.length; j++){
			lst[j].disabled = true;
		}
	}
}
function disableID(cls) {
	var splitCls = cls.split("|");
	for(i = 0; i < splitCls.length; i++){
		document.getElementById(splitCls[i]).checked = false;
		document.getElementById(splitCls[i]).disabled = true;
	}
}
function index(cls,idx){
	var lst = document.getElementsByName(cls);	
		lst[idx].checked = true;
}
function resetDropDown(cls)
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
function addColor(id){
		var element = document.getElementById(id);
		element.style.background = '#99cc00';
}
function removeColor(id){
		if(document.getElementById('None['+id+']').checked && document.getElementById('None2['+id+']').checked ) {
			var element = document.getElementById("tr"+id);
			element.style.background = '';
		}
		
}