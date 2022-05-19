const input = document.getElementById("text_input");
const btn = document.getElementById("btn");

btn.addEventListener("click", copyText);

// CopyText Function
function copyText() {
  input.select();
  document.execCommand("copy");
  btn.innerHTML = "Copied!";
}
