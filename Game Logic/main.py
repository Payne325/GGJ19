from player import Player
from enemy import Enemy
from ctypes import cdll


if __name__ == "__main__":
  
  #Initialise Game Entities

  player_one = Player(
                health=100,
                x_position=1, 
                y_position=1, 
                x_orientation=1.0, 
                y_orientation=1.0, 
                weapon=null, 
                resource=50)



  #Initialise Renderer
  lib = cdll.LoadLibrary('./libfoo.so')
  renderer = lib.GetNewWorld()

  renderer.Begin()

  #while(True):
    #Read user input 

    #Move user to necessary location

    #Perform enemy update

    #Fire player weapon

    #Blit screen


  #End
