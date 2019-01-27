from pyth.player import Player
from pyth.enemy import Enemy
from pyth.weapon import *
from ctypes import cdll, c_float
from pyth.mapgen import MapGen
from pyth.jukebox import Jukebox
import math, random

def enemy_factory(engine, x, y):
    return Enemy(
        health=3,
        x_position=x,
        y_position=y,
        x_orientation=-1,
        y_orientation=-1,
        weapon=Fists(),
        speed=random.randint(1, 4) * 0.01,
        engine=engine)

SPRITE_ZOMBIE = 0
SPRITE_MINE = 1
SPRITE_GUN = 2
SPRITE_GUN_FIRE = 3
SPRITE_HEART = 4
SPRITE_GUN_ZOOM = 5
SPRITE_GUN_ZOOM_FIRE = 6
SPRITE_MINE_ITEM = 7
SPRITE_HEALTH = 8

if __name__ == "__main__":

  #Initialise Renderer
  engine = cdll.LoadLibrary('./target/release/libggj19.so')
  engine.init_engine()

  MapGen(engine, './assets/biggermap.bmp')

  jb = Jukebox(engine)

  #Initialise Game Entities

  player_one = Player(
                health=10,
                x_position=18,
                y_position=18,
                x_orientation=1.0,
                y_orientation=0.0,
                weapon=Gun(),
                resource=50,
				        speed=0.007)

  enemies = []
  mine_drops = []
  health_drops = []
  mines = []

  dt = 0
  bob = 0.0
  while engine.window_is_open():
    while len(mine_drops) < 5:
        x = random.randint(0, 32)
        y = random.randint(0, 32)
        while engine.get_cell_kind(int(x), int(y)) != 0:
            x = random.randint(0, 32)
            y = random.randint(0, 32)
        mine_drops.append((x + 0.5, y + 0.5))

    while len(health_drops) < 5:
        x = random.randint(0, 32)
        y = random.randint(0, 32)
        while engine.get_cell_kind(int(x), int(y)) != 0:
            x = random.randint(0, 32)
            y = random.randint(0, 32)
        health_drops.append((x + 0.5, y + 0.5))

    while len(enemies) < 20:
        x = random.randint(0, 32)
        y = random.randint(0, 32)
        if random.randint(0, 2) == 0:
            x = random.randint(0, 2) * 31
        else:
            y = random.randint(0, 2) * 31
        enemies.append(enemy_factory(engine, x, y))

    #Moves and rotates player as necessary
    player_one.HandleKeys(dt, engine, enemies)
    player_one.Tick(engine, dt)

    #updates the camera location and orientation
    engine.put_camera(c_float(player_one.GetXPosition()), c_float(player_one.GetYPosition()), c_float(player_one.GetOrientationAngle()))

    #Perform enemy update
    deadEnemies = []
    for enemy in enemies:
      enemy.Update(player_one, engine)
      enemy.Tick(engine, dt)
      if enemy.health <= 0:
          enemies.remove(enemy)

    #draw
    engine.draw_world()
    player_one.Draw(1, engine)

    jb.PlayMusic()

    for mine_drop in mine_drops:
        rx = player_one.GetXPosition() - mine_drop[0]
        ry = player_one.GetYPosition() - mine_drop[1]
        dist = math.sqrt(rx * rx + ry * ry)
        engine.draw_sprite(c_float(mine_drop[0]), c_float(mine_drop[1]), c_float(dist), SPRITE_MINE)

        if dist < 0.7:
            mine_drops.remove(mine_drop)
            engine.play_sound(1) # Mine pickup
            player_one.mine_count += 1

    for health_drop in health_drops:
        rx = player_one.GetXPosition() - health_drop[0]
        ry = player_one.GetYPosition() - health_drop[1]
        dist = math.sqrt(rx * rx + ry * ry)
        engine.draw_sprite(c_float(health_drop[0]), c_float(health_drop[1]), c_float(dist), SPRITE_HEALTH)

        if dist < 0.7:
            health_drops.remove(health_drop)
            engine.play_sound(1) # Health pickup
            player_one.health = min(20, player_one.health + 1)

    if len(enemies) == 0:
      print("YOU PROTECTED YOUR HOME! YOU WIN!")
      break
    elif player_one.health == 0:
      print("YOU'RE DEAD AS FUCK! YOU LOSE!")
      break

    for enemy in enemies:
      playerPos = [player_one.GetXPosition(), player_one.GetYPosition()]
      enemyPos = [enemy.GetXPosition(), enemy.GetYPosition()]

      zdist = math.sqrt(
                ((playerPos[0] - enemyPos[0]) * (playerPos[0] - enemyPos[0])) +
                ((playerPos[1] - enemyPos[1]) * (playerPos[1] - enemyPos[1])))

      enemy.Draw(zdist, engine)

    if abs(player_one.x_velocity) > 0.05 or abs(player_one.y_velocity) > 0.05:
        bob += 0.3
    if engine.get_key(7):
        if player_one.attack_cooldown < 5:
            engine.draw_decal(400 - 128, 600 - 512, SPRITE_GUN_ZOOM_FIRE)
        else:
            engine.draw_decal(400 - 128, 600 - 512, SPRITE_GUN_ZOOM)
    else:
        if player_one.attack_cooldown < 5:
            engine.draw_decal(400 - 128, 600 - 256 + int((math.cos(bob) + 1.0) * 10.0), SPRITE_GUN_FIRE)
        else:
            engine.draw_decal(400 - 128, 600 - 256 + int((math.cos(bob) + 1.0) * 10.0), SPRITE_GUN)

    for i in range(player_one.health):
        engine.draw_decal(16 + 32 * i, 16, SPRITE_HEART)

    for i in range(player_one.mine_count):
        engine.draw_decal(16 + 16 * i, 64, SPRITE_MINE_ITEM)

    dt = engine.update_window()
  #End
