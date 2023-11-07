let xhttp;

document.addEventListener("DOMContentLoaded",init,false)

function init () {
    let form = document.querySelector("form")
    form.addEventListener("submit",store_keys,false)
}

function store_keys (event) {
    let data = new FormData();
    data.append("continueKey", document.getElementById("continueKey").value)
    data.append("shootKey", document.getElementById("shootKey").value)
    data.append("hitKey", document.getElementById("hitKey").value)
    data.append("skipKey", document.getElementById("skipKey").value)
    data.append("invincibleKey", document.getElementById("invincibleKey").value)
    
    console.log(document.getElementById("continueKey").value,document.getElementById("shootKey").value)
    xhttp = new XMLHttpRequest();
    xhttp.addEventListener("readystatechange", handle_response, false);
    xhttp.open("POST", "/~bc23/cgi-bin/ca2/run.py/store_keys", true);  //       /~bc23/cgi-bin/ca2/run.py
    xhttp.send(data);
    
}


function handle_response() {
    //   https://www.w3schools.com/jsref/met_loc_reload.asp
    location.reload()
}