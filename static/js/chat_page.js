let timeoutID;
let timeout = 15000;

function setup() {
    document.getElementById("button").addEventListener("click", newMessage);
    document.getElementById("button").addEventListener("keypress", checkKey);
    timeoutID = window.setTimeout(poller, timeout);
    poller();
}

function newMessage() {
    const author = document.getElementById("username").value;
    const message = document.getElementById("mssg").value;
    
    fetch("/new_message/", { 
        method: "POST",
        headers: { "Content-type": "application/x-www-form-urlencoded; charset=UTF-8" },
        body: `username=${author}&message=${message}` 
        })
        .then((response) => {
            return response.json();
        })
        .then((result) => {
            displayMessages(result);
            clearInput();
        })
        .catch(() => {
            console.log("Error posting new message!");
        })
}

function displayMessages(results) {
    let chat_window = document.getElementById("chat_window");
    let messages = "";
    for (let index in results) {
        current_set = results[index]; 
        for (let key in current_set) {
            let author = key;
            let message = current_set[key];
            messages += `${author}:\n${message}\n\n`;
        } 
    }
    chat_window.value = messages;
    timeoutID = window.setTimeout(poller, timeout);
}

function clearInput() {
    const messageInput = document.getElementById("mssg");
    messageInput.value = "";
}

function poller() {
    fetch("/messages/") 
        .then((response) => {
            return response.json();
         })
        .then((results) => {
            displayMessages(results);
         })
        .catch(() => {
            let chat_window = document.getElementById("chat_window");
            chat_window.value = "error retrieving messages from server";
        })
}

function checkKey(e) {
    if (e.key === "Enter") {
        button.click();
    }
}

window.addEventListener("load", setup);
