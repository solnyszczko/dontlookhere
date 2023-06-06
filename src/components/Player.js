import Entity from './Entity';

class Player extends Entity {
    inventory = [];

    attributes = {
        name: 'Player',
        ascii: '@',
        color: 'red',
        health: 10,
        damage: 1,
        armor: 5
    }

    move(dx, dy) {
        // don't allow to move if player is dead
        if (this.attributes.health <=0) return;
        this.x += dx;
        this.y += dy;
    }

    add(item) {
        this.inventory.push(item);
    }

    copyPlayer() {
        let newPlayer = new Player();
        Object.assign(newPlayer, this);
        return newPlayer;
    }
}

export default Player;