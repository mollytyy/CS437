var server_port = 65432;
var server_addr = "192.168.137.100";   // the IP address of your Raspberry PI

var socket = null;

function setup_connection() {
    const net = require("net");

    socket = net.createConnection({ port: server_port, host: server_addr }, () => {
        console.log("connected to server!");
        socket.setEncoding("utf-8");
    });

    socket.on("data", (data) => {
        var str = data.toString()
        var temperature_label = document.getElementById("temperature_label");
        var battery_label = document.getElementById("battery_label");

        if (str.includes("Temperature")) {
            temperature_label.innerText = str;
        } else if (str.includes("Battery")) {
            battery_label.innerText = str;
        }
    });

    socket.on("end", () => {
        console.log("disconnected from server");
    });
}

function destroy_connection() {
    socket.disconnect();
    socket.destroy();
}

function send_message(message) {
    if (socket != null) {
        socket.write(message);
        console.log(message);
    }
}

function directions(element) {
    send_message(element.id);
    console.log(`${element.id} message sent`);
}

function stop() {
    send_message("stop");
    console.log("stop message sent");
}