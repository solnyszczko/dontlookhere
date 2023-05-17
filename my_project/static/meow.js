var display = new ROT.Display({width:60, height:60});
document.body.appendChild(this.display.getContainer());
this.display.draw(20,  20, "@", "#0f0");
this.display.draw(20,  21, "@", "#0f0");
//console.log("meow")
let keyBindings = {
    up: "ArrowUp",
    left: "ArrowLeft",
    right: "ArrowRight",
    down: "ArrowDown"
  };



document.addEventListener("keydown", (event) => {
 //   console.log(event.code)
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

  
  function update_display(game_state) {
  //  console.log("meow")
    console.log(game_state)
   console.log(typeof game_state)
  //  console.log(game_state.players)
  //  console.log("meowmeow")
    display.clear()
    display.draw(22,  23, "@", "#0f0")
    for (const character in game_state) {
        console.log(game_state[character])
        const noob = game_state[character]
      //  console.log(character.players)
        // Get character properties
      //  const name = character.name
        console.log("meow")
    //    const color = character.color;
        
        // Draw the character
        display.draw(noob.x,  noob.y, "@", "#0f0")
     
      }



}
  

var client_id = Date.now()
document.querySelector("#ws-id").textContent = client_id;
var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
ws.onmessage = function(event) {
 //   console.log(event.data)
    const game_state_parsed = JSON.parse(event.data)
    update_display(game_state_parsed)
   // console.log("MEOW")
 //   var messages = document.getElementById('messages')
   // var message = document.createElement('li')
   // var content = document.createTextNode(event.data)
   // message.appendChild(content)
   // messages.appendChild(message)
};
function sendMessage(event) {
    var input = document.getElementById("messageText")
    ws.send(input.value)
    input.value = ''
    event.preventDefault()
}