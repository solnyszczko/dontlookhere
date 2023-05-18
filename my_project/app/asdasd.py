Generate me some python code for a roguelike game system and loop:
```python
import random
class Player:
 def \_\_init\_\_(self, x, y):
 self.x = x
 self.y = y
 self.health = 100
 self.attack\_power = 5
 self.defense\_power = 3
 self.speed = 2
 self.inventory = []
 def move(self, dx, dy):
 self.x += dx
 self.y += dy
 def attack(self, monster):
 if monster.health <= self.attack\_power:
 monster.health -= self.attack\_power
 else:
 print("You missed!")
 def defense(self, projectile):
 if projectile.damage <= self.defense\_power:
 self.health -= projectile.damage
 else:
 print("You take minimal damage.")
 def loop(self):
 while True:
 print("You are at ({}, {})".format(self.x, self.y))
 print("Your health is {}/100".format(self.health))
 print("Your attack power is {}".format(self.attack\_power))
 print("Your defense power is {}".format(self.defense\_power))
 print("Your speed is {}".format(self.speed))
 print("Inventory:")
 for item in self.inventory:
 print("- {} ({})".format(item[0], item[1]))
 print("\nAvailable inventory items:")
 for item in get\_available\_items():
 print("- {} ({})".format(item[0], item[1]))
 print()
 # Move player
 dx, dy = get\_movement\_input()
 self.move(dx, dy)
 # Attack monster
 if is\_monster\_in\_range(self):
 monster = get\_nearest\_monster()
 attack\_success = False
 while not attack\_success:
 print("You are fighting {}!".format(monster[0]))
 attack\_success = self.attack(monster)
 # Defend against projectile
 if is\_projectile\_in\_range(self):
 projectile = get\_nearest\_projectile()
 defense\_success = False
 while not defense\_success:
 print("You are hit by a {}!".format(projectile[0]))
 defense\_success = self.defense(projectile)
 # Get inventory input
 item1, item2 = get\_inventory\_input()
 if item1 and item2:
 self.inventory.append((item1, item2))
 print("You pick up {} ({}) and {} ({})".format(item1[0], item1[1], item2[0], item2[1]))
 # Get movement input until player exits game or reaches goal
 while True:
 dx, dy = get\_movement\_input()
 self.move(dx, dy)
 if is\_player\_at\_goal():
 break
 print("You exit the dungeon!")
# Main loop
while True:
 player = Player(\*get\_starting\_position())
 while not player.health or is\_game\_over():
 player.loop()
 get\_input("\nContinue? (y/n): ")
 if input().lower() == "n":
 break
# Get available items and monsters
available\_items = []
for item in get\_all\_items():
 if not item[1]["rare"]:
 available\_items.append(item)
monster\_data = [("Zombie", 20, 5), ("Skeleton", 30, 4)]
available\_monsters = []
for monster in monster\_data:
 if not get\_inventory\_item(monster[1]):
 available\_monsters.append(monster)
# Get starting position and goal
starting\_position = (2, 2)
goal = None
while True:
 print("Enter starting position (x,y):")
 x, y = map(int, input().split())
 if not is\_valid\_position(x, y):
 continue
 while True:
 goal = get\_