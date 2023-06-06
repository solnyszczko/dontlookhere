import Loot from './Loot';
import Monster from './Monster';
import Stairs from './Stairs';

const lootTable = [
    { name: 'Long Sword', color: 'darkgrey', ascii: '/', offset: { x: 6, y: 3 }, damage: 1 },
    { name: 'Health Potion', color: 'red', ascii: '!', offset: { x: 6, y: 3 }, health: 10 },
    { name: 'Gold Coin', color: 'yellow', ascii: '$', offset: { x: 3, y: 3 } },
    { name: 'Light Armor', color: 'lightgrey', ascii: '#', offset: { x: 4, y: 3 }, armor: 1 }
]

const monsterTable = [
    { name: 'Ogre', color: 'darkgreen', ascii: 'O', offset: { x: 2, y: 3 }, health: 6, damage: 1 },
    { name: 'Kolbold', color: 'orange', ascii: 'M', offset: { x: 4, y: 3 }, health: 3, damage: 1 },
    { name: 'Slime', color: 'lightgreen', ascii: '-', offset: { x: 3, y: 2 }, health: 2, damage: 1 },
    { name: 'Dragon', color: 'blue', ascii: 'W', offset: { x: 2, y: 3 }, health: 10, damage: 2 }
]

class Spawner {
    constructor(world) {
        this.world = world;
    }

    spawn(spawnCount, createEntity) {
        for (let count = 0; count < spawnCount; count++) {
            let entity = createEntity();
            this.world.add(entity);
            this.world.moveToSpace(entity);
        }
    }

    spawnLoot(spawnCount) {
        this.spawn(spawnCount, () => {
            return new Loot(
                getRandomInt(this.world.width - 1),
                getRandomInt(this.world.height - 1),
                this.world.tilesize,
                lootTable[getRandomInt(lootTable.length)]
            );
        })
    }

    spawnMonsters(spawnCount) {
        this.spawn(spawnCount, () => {
            return new Monster(
                getRandomInt(this.world.width -1),
                getRandomInt(this.world.height - 1),
                this.world.tilesize,
                monsterTable[getRandomInt(lootTable.length)]
            );
        })
    }

    spawnStairs() {
        let stairs = new Stairs(this.world.width - 10, this.world.height - 10, this.world.tilesize);
        this.world.add(stairs);
        this.world.moveToSpace(stairs);
    }
}

function getRandomInt(max) {
    return Math.floor(Math.random() * Math.floor(max));
}

export default Spawner;