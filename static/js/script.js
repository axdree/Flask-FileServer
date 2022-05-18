document.querySelector("html").classList.add("js");

var fileInput = document.querySelector(".input-file"),
	button = document.querySelector(".input-file-trigger"),
	the_return = document.querySelector(".file-return"),
    upload = document.querySelector(".upload-file");

button.addEventListener("keydown", function (event) {
	if (event.keyCode == 13 || event.keyCode == 32) {
		fileInput.focus();
	}
});
button.addEventListener("click", function (event) {
	fileInput.focus();
	return false;
});
fileInput.addEventListener("change", function (event) {
    if(this.value.length > 0){
        the_return.innerHTML = fileInput.files[0].name;
    }else{
        the_return.innerHTML = "None";
    }
});
fileInput.addEventListener("change", function (event) {
    if(the_return.innerHTML != "None"){
        upload.removeAttribute("hidden");
    }
});

