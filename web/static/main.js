function start_service(){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(){
        if(this.readyState == 4 && this.status == 200) {
            document.getElementById("service_status").innerHTML = this.responseText;
        }
    }
    xhttp.open("POST", "start_service", true);
    xhttp.send();
}

function stop_service(){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function(){
        if(this.readyState == 4 && this.status == 200) {
            document.getElementById("service_status").innerHTML = this.responseText;
        }
    }
    xhttp.open("POST", "stop_service", true);
    xhttp.send();
}

function set_device(){
    var xhttp = new XMLHttpRequest();
    var device_path = document.getElementById("device_list").value
    xhttp.onreadystatechange = function(){
        if(this.readyState == 4 && this.status == 200) {
            alert("Complete");
        }
    }
    xhttp.open("POST", "set_device", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    xhttp.send("device_path="+device_path);
}