window.addEventListener("load", ()=>{
	form = document.querySelector("#mainForm");
	img = document.querySelector("#qrimg");
	form.addEventListener("submit", (e)=>{
		if (e.preventDefault) e.preventDefault();
		msg = document.getElementById("msg").value;	
		img.src = `${form.action}?msg=${msg}`
		img.style.display = "inline";
		return false;
	});
});
