//Activa la visibilidad del elemento con id "popup+num"
function showPopUp(popupId) {
	var state = document.getElementById(popupId).style.visibility;
	if (state == "visible"){
		document.getElementById(popupId).style.visibility= "hidden";
	}else{
		document.getElementById(popupId).style.visibility= "visible";
	}
}

var map = document.getElementById("mapa-Box2");
map.addEventListener("click", changePinLocation);

function changePinLocation(e) {
	var cursorX = (e.pageX - e.currentTarget.offsetLeft - 25).toString() + "px";
    var cursorY = (e.pageY - e.currentTarget.offsetTop - 37).toString() + "px";
	document.getElementById("location-Pin").style.marginLeft = cursorX;
	document.getElementById("location-Pin").style.marginTop = cursorY;
}

function getCoordinates() {
	var X = document.getElementById("location-Pin").style.marginLeft;
    var Y = document.getElementById("location-Pin").style.marginTop;
	$.ajax({
        method:'GET',
		url: '/updateCoordinates',
        data:{
            "CoorX": X,
            "CoorY": Y
        }
    });
	location.href = '/';
}

function changeColor(cat) {
	var categoriaButton = document.getElementById(cat);
	categoriaButton.style.backgroundColor = "#015554";
	categoriaButton.style.color = "white";
} 