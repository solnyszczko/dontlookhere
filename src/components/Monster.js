import Entity from './Entity';

class Monster extends Entity {
    action(verb, world) {
        if (verb === 'bump') {
            world.addToHistory(`Player attacks ${this.attributes.name}!`);
            this.attributes.health = this.attributes.health - world.player.attributes.damage;
            if (this.attributes.health <= 0) {
                world.addToHistory(`${this.attributes.name} is dead!`);
                world.remove(this);
            } else {
                world.addToHistory(`${this.attributes.name}'s health is ${this.attributes.health}`);
                if (world.player.attributes.armor >= 0) {
                    let totalDamage = this.attributes.damage - world.player.attributes.armor;
                    world.player.attributes.armor = world.player.attributes.armor - (Math.min(this.attributes.damage, world.player.attributes.armor));
                    if (totalDamage > 0) {
                        world.player.attributes.health = world.player.attributes.health - totalDamage;
                    }
                } else {
                    world.player.attributes.health = world.player.attributes.health - this.attributes.damage;
                }
            }
            if (world.player.attributes.health <= 0) {
                world.addToHistory('You have died!');
                world.player.attributes.ascii = '*';
                world.player.attributes.offset = { x: 2, y: 6 };
            } else {
                world.addToHistory(`You have ${world.player.attributes.armor} armor left!`);
                world.addToHistory(`You have ${world.player.attributes.health} health left!`);
            }
        }
    }
}

export default Monster;