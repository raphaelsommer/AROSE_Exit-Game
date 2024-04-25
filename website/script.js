function revealContent() {
    var secretCode = document.getElementById("secretCode").value;
    var extraContent = document.getElementById("extraContent");

    if (secretCode === "1234") { // Replace "1234" with your specific code
        extraContent.classList.remove("hidden");
        extraContent.classList.add("visible");
    } else {
        alert("Wrong code!");
    }
}
