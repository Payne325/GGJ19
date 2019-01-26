from pyth.player import Player
from pyth.enemy import Enemy
from pyth.weapon import *
from ctypes import cdll, c_float
import math

if __name__ == "__main__":

  #Initialise Renderer
  engine = cdll.LoadLibrary('./target/release/libggj19.so')
  engine.init_engine()

  #Initialise Game Entities

  player_one = Player(
                health=100,
                x_position=2,
                y_position=2,
                x_orientation=1.0,
                y_orientation=0.0,
                weapon=Fists(),
                resource=50,
				        speed=0.007)

  #populate enemies
  enemy_one = Enemy(
                health=100,
                x_position=11,
                y_position=11,
                x_orientation=-1,
                y_orientation=-1,
                weapon=Fists(),
                speed=0.02,
                engine=engine)

  enemies = [enemy_one]

  dt = 0.0
  while engine.window_is_open():

    #Moves and rotates player as necessary
    player_one.HandleKeys(dt, engine, enemies)
    player_one.Tick(dt)

    #updates the camera location and orientation
    engine.put_camera(c_float(player_one.GetXPosition()), c_float(player_one.GetYPosition()), c_float(player_one.GetOrientationAngle()))

    #Perform enemy update
    for enemy in enemies:
      enemy.Update(player_one)
      enemy.Tick(dt)

    engine.draw_world()
    player_one.Draw(1, engine)

    for enemy in enemies:
      playerPos = [player_one.GetXPosition(), player_one.GetYPosition()]
      enemyPos = [enemy.GetXPosition(), enemy.GetYPosition()]

      zdist = math.sqrt(
                ((playerPos[0] - enemyPos[0]) * (playerPos[0] - enemyPos[0])) +
                ((playerPos[1] - enemyPos[1]) * (playerPos[1] - enemyPos[1])))

      enemy.Draw(zdist, engine)

    dt = engine.update_window()
  #End
