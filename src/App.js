import React, { Component,useRef, useEffect  } from 'react';
import logo from './logo.svg';
import ROT from 'rot-js';
import './App.css';
import ReactRogue from './components/ReactRogue';
import phaserGame from './PhaserGame'
import HelloWorldScene from './scenes/HelloWorldScene'

const handleClick = () => {
  const scene = phaserGame.scene.keys.helloworld 
  scene.createEmitter()
}

const Gamer = () => {
  const mainRef = useRef(null);

  useEffect(() => {
    // Access the main element using the ref
    const mainElement = mainRef.current;
  //  var main_display = new ROT.Display({ width: 10, height: 10 });






  
    // Perform any necessary operations on the main element

    // Example: Set innerHTML of the main element
    mainElement.innerHTML = 'Example Content';

    // Example: Append a child element to the main element
    const childElement = document.createElement('div');
    childElement.textContent = 'Child Elemsdfent';
    mainElement.appendChild(childElement);
 //   mainElement.appendChild(main_display.getContainer());
  }, []);

  return <div ref={mainRef}></div>;
};



class App extends Component {
  render() {
    return (
      <div className="App">
        <div className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h2>Welcome to React</h2>
        </div>
        <div className="grid-container">
        <div className="item-1" id="main">desu
        <handleClick />

        
        </div>
        <div className="item-2" id="info"></div>
        <div className="item-3" id="lol"></div>


        </div>
      </div>
    );
  }
}

export default App;


//<Gamer />
//<ReactRogue width={40} height={40} tilesize={16} />