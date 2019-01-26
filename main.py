from pyth.player import Player
from pyth.enemy import Enemy
from pyth.weapon import *
from ctypes import cdll, c_float


if __name__ == "__main__":

  #Initialise Game Entities

  player_one = Player(
                health=100,
                x_position=1,
                y_position=1,
                x_orientation=1.0,
                y_orientation=0.0,
                weapon=Fists(),
                resource=50,
				speed=0.1)

  #populate enemies
  enemies = []

  #Initialise Renderer
  engine = cdll.LoadLibrary('./target/release/libggj19.so')
  engine.init_engine()

  while engine.window_is_open():
    #Moves and rotates player as necessary
    player_one.HandleKeys(engine, enemies)
    #updates the camera location and orientation
    engine.put_camera(c_float(player_one.GetXPosition()), c_float(player_one.GetYPosition()), c_float(player_one.GetOrientationAngle()))

    #Perform enemy update
    for enemy in enemies:
      break

    engine.draw_world()
    engine.update_window()


  #End
