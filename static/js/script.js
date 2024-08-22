/* DROPDOWN FOR MORE */
function dropdownMore() {
    document.getElementById("myDropdown").classList.toggle("show");
}


window.onclick = function(event) {
    if (!event.target.matches('.dropbtn') && !event.target.closest('.dropbtn')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        for (var i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}
/*****/

// MODAL WINDOW
var modal = document.getElementById("modalCreatePost");
var btn = document.getElementById("openPostCreate");
var span = document.getElementsByClassName("close-btn")[0];

btn.onclick = function() {
    modal.style.display = "block";
    console.log("clicked");
}

window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

span.onclick = function() {
    modal.style.display = "none";
}

///////////////////