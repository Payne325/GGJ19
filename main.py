from ctypes import cdll, c_float
from pyth.mapgen import MapGen
from pyth.jukebox import Jukebox
from pyth.factory import Factory
from pyth.globals import *
import math, random
import os

if __name__ == "__main__":

  difficulty = 1.0
  #Initialise Renderer
  path = './target/release/libggj19.so'
  print(os.name)
  if os.name == "nt":
	  path = './target/x86_64-pc-windows-gnu/release/ggj19.dll'
  engine = cdll.LoadLibrary(path)

  engine.init_engine()

  MapGen(engine, './assets/biggermap.bmp')

  jb = Jukebox(engine)

  #Initialise Game Entities

  player_one = Factory.CreatePlayer(engine)

  enemies = []
  mine_drops = []
  health_drops = []
  mines = []

  spawn_points = [
      (77, 7),
      (25, 33),
      (14, 94),
      (62, 46),
      (46, 20),
      (6, 65),
	  (38, 48),
	  (36, 55),
	  (75, 99),
	  (50, 98),
	  (7, 95),
	  (64, 51),
  ]

  dt = 0
  bob = 0.0
  while engine.window_is_open():
    while len(mine_drops) < 10:
        x = random.randint(0, 128)
        y = random.randint(0, 128)
        while engine.get_cell_kind(int(x), int(y)) != 0:
            x = random.randint(0, 128)
            y = random.randint(0, 128)
        mine_drops.append((x + 0.5, y + 0.5))

    while len(health_drops) < 10:
        x = random.randint(0, 128)
        y = random.randint(0, 128)
        while engine.get_cell_kind(int(x), int(y)) != 0:
            x = random.randint(0, 128)
            y = random.randint(0, 128)
        health_drops.append((x + 0.5, y + 0.5))


    while len(enemies) < 20:
        spawn_idx = random.randint(0, len(spawn_points) - 1)
        x = spawn_points[spawn_idx][0]
        y = spawn_points[spawn_idx][1]
        #while engine.get_cell_kind(int(x), int(y)) != 0:
        #    x = random.randint(0, 32)
        #    y = random.randint(0, 32)
        #if random.randint(0, 2) == 0:
        #    x = random.randint(0, 2) * 31
        #else:
        #    y = random.randint(0, 2) * 31
        enemies.append(Factory.CreateEnemy(engine, x + 0.5, y + 0.5, difficulty))
        difficulty += 0.1

    #Moves and rotates player as necessary
    player_one.HandleKeys(dt, enemies)
    player_one.Tick(dt)

    #updates the camera location and orientation
    engine.put_camera(c_float(player_one.GetXPosition()), c_float(player_one.GetYPosition()), c_float(player_one.GetOrientationAngle()))

    #Perform enemy update
    deadEnemies = []
    for enemy in enemies:
      enemy.Update(player_one)
      enemy.Tick(dt)
      if enemy.health <= 0:
          enemies.remove(enemy)
          engine.play_sound(15)

    #draw
    engine.draw_world()
    player_one.Draw(1)

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

      enemy.Draw(zdist)

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

  while engine.window_is_open():
    if engine.get_key(6):
        engine.close_engine()
        break
    engine.draw_decal(400 - 128, 300 - 127, SPRITE_GAME_OVER)
    engine.update_window()
  #End
