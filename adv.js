function userCreateChoice(){
	document.getElementById("userSubmitChoice").submit();
}

function selectOption(destination){
	gotoPage(destination);
}

function gotoPage(destination){
	window.location.replace('/adv/' + destination);
}
