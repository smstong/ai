window.addEventListener("load", ()=>{
	const form = document.querySelector("#mainForm");
	const canvas = document.getElementById("can");
	form.addEventListener("submit", async (e)=>{
		if (e.preventDefault) e.preventDefault();
		const qr = await fetchQR(form.action);
		const img = document.createElement("img");
		img.onload = ()=>{
			canvas.width = img.width;
			canvas.height = img.height;
			const ctx = canvas.getContext('2d');
			ctx.drawImage(img, 0, 0);
		};
		img.src = URL.createObjectURL(qr);
		return false;
	});
});

async function fetchQR(url){

	const formData = new FormData();
	const bgFileE = document.getElementById("bg");

	const msg = document.getElementById("msg").value;	
	formData.append("msg", msg);
	formData.append("bg", bgFileE.files[0]);

	const response = await fetch(url, {
		method: "POST",
		mode: "cors",
		body: formData,
	});

	const qr = await response.blob();
	return qr;
}
