import Phaser from 'phaser'

export default class HelloWorldScene extends Phaser.Scene {
  constructor() {
    super('helloworld')
  }

  preload() {
    this.load.setBaseURL('localhost:3000/')

    this.load.image('logo', 'assets/sprites/asuna.png')
    this.load.image('red', 'assets/particles/arrow.png')
  }

  create() {
    this.createEmitter()
  }

  createEmitter() {
    const particles = this.add.particles('red')

    const emitter = particles.createEmitter({
      speed: 100,
      scale: { start: 1, end: 0 },
      blendMode: 'ADD',
    })

    const logo = this.physics.add.image(400, 100, 'logo')

    logo.setVelocity(100, 200)
    logo.setBounce(1, 1)
    logo.setCollideWorldBounds(true)

    emitter.startFollow(logo)
  }
}
