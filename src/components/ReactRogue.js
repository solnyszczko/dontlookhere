import React, { useRef, useEffect, useState } from 'react';
import InputManager from './InputManager';
//import Player from './Player';
import World from './World';
import Spawner from './Spawner';

const ReactRogue = ({ width, height, tilesize }) => {
    const canvasRef = useRef();
    const [world, setWorld] = useState(new World(width, height, tilesize));
    let inputManager = new InputManager();
    const handleInput = (action, data) => {
        console.log(`handleInput: ${action}:${JSON.stringify(data)}`);
        let newWorld = new World();
        Object.assign(newWorld, world);
        newWorld.movePlayer(data.x, data.y);
        setWorld(newWorld);
    };

    useEffect(() => {
        console.log('Create Map');
        let newWorld = new World();
        Object.assign(newWorld, world);
        newWorld.createCellularMap();
        newWorld.moveToSpace(world.player);
        let spawner = new Spawner(newWorld);
        spawner.spawnLoot(10);
        spawner.spawnMonsters(6);
        spawner.spawnStairs();
        setWorld(newWorld);
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    useEffect(() => {
        console.log('Bind Input');
        inputManager.bindKeys();
        inputManager.subscribe(handleInput);
        return () => {
            inputManager.unbindKeys();
            inputManager.unsubscribe(handleInput);
        }
    });

    useEffect(() => {
        console.log('Draw to canvas');
        const ctx = canvasRef.current.getContext('2d');
        ctx.clearRect(0, 0, width * tilesize, height * tilesize);
        world.draw(ctx);
    });

    return (
        <div>
            <canvas
                ref={canvasRef}
                width={width * tilesize}
                height={height * tilesize}
                style={{ border: '1px solid black', background: 'dimgrey' }}>
            </canvas>
            <ul>
                {world.player.inventory.map((item, index) => (<li key={index}>{item.attributes.name}</li>))}
            </ul>
            <ul>
                {world.history.map((item, index) => (<li key={index}>{item}</li>))}
            </ul>

        </div>
    )
}

// const ReactRogue = props => (
//     <canvas
//     width={props.width * props.tilesize}
//     height={props.height * props.tilesize}
//     style={{border: '1px solid black'}}
//     ></canvas>
// );

export default ReactRogue;