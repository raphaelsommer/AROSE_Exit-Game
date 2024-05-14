var clickedLink = false;

        function resetOpacity() {
            clickedLink = true;
        }

        window.addEventListener("scroll", function() {
            var scrollPosition = window.scrollY || window.pageYOffset;
            var scale = 1 + (scrollPosition / window.innerHeight);
            var opacity = Math.min(scrollPosition / (window.innerHeight / 2), 1);
            console.log(scrollPosition, clickedLink);

            if (scale < 2) {
                if (clickedLink) {
                    document.getElementById("nav-bar").style.opacity = 1;
                    document.getElementById("logo").style.opacity = 1;
                    document.getElementById("background-container").style.opacity = 0.2 + opacity;
                    document.getElementById("background").style.transform = `scale(${scale})`;
                } else {
                    document.getElementById("nav-bar").style.opacity = opacity;
                    document.getElementById("logo").style.opacity = opacity;
                    document.getElementById("background-container").style.opacity = 0.2 + opacity;
                    document.getElementById("background").style.transform = `scale(${scale})`;
                }
            }
            
        });

        function revealContent() {
            var secretCode = document.getElementById("secretCode").value;
            var extraContent = document.getElementById("extraContent");
            //var input = document.getElementsById("input");

            if (secretCode === "AROSE") { 
                extraContent.classList.remove("Anleitung_hiddenContent");
                extraContent.classList.add("Anleitung_visibleContent");
                input.classList.remove("Anleitung_Input");
                input.classList.add("Anleitung_hiddenInput");
            } else {
                alert("In a garden where secrets sleep, Under moon’s watchful eyes, I keep. From whispers low, within the dark, With dawn’s first light, my life doth spark. Not plant, nor flower, yet I bloom, Rising silently from night’s gloom. What am I, that with light grows? Think carefully, the answer AROSE.");
            }
        }