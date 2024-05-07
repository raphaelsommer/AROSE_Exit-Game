function revealContent() {
    var secretCode = document.getElementById("secretCode").value;
    var extraContent = document.getElementById("extraContent");
    //var input = document.getElementsById("input");

    if (secretCode === "1234") { 
        extraContent.classList.remove("Spielanleitung_hiddenContent");
        extraContent.classList.add("Spielanleitung_visibleContent");
        //input.classList.remove("Spielanleitung_Eingabe");
        //input.classList.add("Spielanleitung_hiddenEingabe");
    } else {
        alert("Wrong code!");
    }
}