var display = new ROT.Display({width:20, height:5});
document.body.appendChild(this.display.getContainer());


let keyBindings = {
    up: "ArrowUp",
    left: "ArrowLeft",
    right: "ArrowRight",
    down: "ArrowDown"
  };



document.addEventListener("keydown", (event) => {
    if (event.code === keyBindings.up) {
        ws.send("up")
    } else if (event.code === keyBindings.left) {
        ws.send("left")
    } else if (event.code === keyBindings.right) {
        ws.send("right")
    } else if (event.code === keyBindings.down) {
        ws.send("down")
    }
  });

  
var client_id = Date.now()
document.querySelector("#ws-id").textContent = client_id;
var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
ws.onmessage = function(event) {
    var messages = document.getElementById('messages')
    var message = document.createElement('li')
    var content = document.createTextNode(event.data)
    message.appendChild(content)
    messages.appendChild(message)
};
function sendMessage(event) {
    var input = document.getElementById("messageText")
    ws.send(input.value)
    input.value = ''
    event.preventDefault()
}