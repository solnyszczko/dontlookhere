import Entity from './Entity';

class Loot extends Entity {
    action(verb, world) {
        if (verb === 'bump') {
            world.player.add(this);
            world.remove(this);
            if (this.attributes.health) {
                world.player.health += this.attributes.health;
                world.addToHistory(`Your health has improved by ${this.attributes.health}!`);
            } else  if (this.attributes.armor) {
                world.player.armor += this.attributes.armor;
                world.addToHistory(`Your armor has improved by ${this.attributes.armor}!`);
            } else  if (this.attributes.damage) {
                world.player.damage += this.attributes.damage;
                world.addToHistory(`Your damage has improved by ${this.attributes.damage}!`);
            };
        }
        if (verb === 'drop') {
            console.log('drop', this);
        }
    }
}

export default Loot;