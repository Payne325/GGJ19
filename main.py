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
    while len(mines) < 10:
        mines.append(Factory.CreateMine(engine))

    while len(health_drops) < 10:
        health_drops.append(Factory.CreateHealthPack(engine))

    while len(enemies) < 20:
        spawn_idx = random.randint(0, len(spawn_points) - 1)
        x = spawn_points[spawn_idx][0]
        y = spawn_points[spawn_idx][1]
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

    jb.PlayMusic()

    for mine in mines:
      mine.Draw(player_one)

      if mine.HasCollidedWith(player_one):
        mines.remove(mine)
        mine.PerformCollisionAction(player_one)

    for health_drop in health_drops:
        health_drop.Draw(player_one)

        if health_drop.HasCollidedWith(player_one):
            health_drops.remove(health_drop)
            health_drop.PerformCollisionAction(player_one)

    if len(enemies) == 0:
      print("YOU PROTECTED YOUR HOME! YOU WIN!")
      break
    elif player_one.health == 0:
      print("YOU'RE DEAD AS FUCK! YOU LOSE!")
      break

    for enemy in enemies:
     enemy.Draw(player_one)

    player_one.Draw(player_one)

    dt = engine.update_window()

  while engine.window_is_open():
    if engine.get_key(6):
        engine.close_engine()
        break
    engine.draw_decal(400 - 128, 300 - 127, SPRITE_GAME_OVER)
    engine.update_window()
  #End
