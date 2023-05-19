var display = new ROT.Display({width:60, height:40});
document.body.appendChild(this.display.getContainer());
//this.display.draw(2,  2, "B", "#0f0");

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
    console.log(game_state)

    display.clear()

    for (const character in game_state) {
        console.log(game_state[character])
        const noob = game_state[character]
        console.log(typeof noob.x)
        x = parseInt(noob.x)
        y = parseInt(noob.y)
 
        // Draw the character
        display.draw(x,  y, "@", "#0f0")
     
      }



}
  

var client_id = Date.now()
document.querySelector("#ws-id").textContent = client_id;
var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);

ws.onmessage = function(event) {
 //   console.log(event.data)
    const game_state_parsed = JSON.parse(event.data)
    console.log(event)
    update_display(game_state_parsed)

};
