from pyth.pawn import Pawn
from pyth.state_machine import State_Machine
from pyth.pathfinder import Pathfinder
from pyth.drawable import Drawable
from pyth.globals import *
import math

class Enemy(Pawn, Drawable):
  def __init__(self, health, x_position, y_position, x_orientation, y_orientation, weapon, speed, engine):
    Pawn.__init__(self, health, x_position, y_position, x_orientation, y_orientation, weapon, speed)
    Drawable.__init__(self)
    #self.state_machine = State_Machine(sightRange)
    self.pathfinder = Pathfinder(engine)
    self.img = ENEMY_SPRITE_INDEX

    self.prev_x = -1
    self.prev_y = -1

  def Update(self, targetPawn):
    #self.state_machine.Update(self.x_position, self.y_position, targetPawn)

    if(self.prev_x != self.x_position or self.prev_y != self.y_position):
      target_x = targetPawn.GetXPosition()
      target_y = targetPawn.GetYPosition()

      new_velocity = self.pathfinder.GetNewVelocity(self.x_position, self.y_position, target_x, target_y)
      self.x_velocity = new_velocity[0]
      self.y_velocity = new_velocity[1]
    
      #normalise velocity and set x & y orientation
      magnitude = math.sqrt((self.x_velocity*self.x_velocity) + (self.y_velocity*self.y_velocity))
      self.x_orientation = self.x_velocity/magnitude
      self.y_orientation = self.y_velocity/magnitude

  def Draw(self, z_dist, engine):
    engine.draw_sprite(self.x_position, self.y_position, z_dist, self.img) 
