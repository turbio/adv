editMode = false;

function userCreateAction(){
	if(!editMode){
		editMode = true;
		document.getElementById("actionEntry").style.display = "block";
		//document.getElementById("actionEntry").style.transform = "translate(0, 0)";
		//document.getElementById("actionEntry").style.opacity = "1";
		document.getElementById("addOptionTextBox").style.display = "none";
		document.getElementById("sendIcon").style.opacity = "1";
		document.getElementById("editIcon").style.opacity = "0";
		document.getElementById("addIcon").style.opacity = "0";		
	}else{

	}
}

function selectOption(destination){
	if (window.location.href.indexOf("adv/") == -1){
		destination = 'adv/' + destination
	}
	window.location.replace(destination);
}