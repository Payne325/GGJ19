from pyth.collidable import Collidable
from pyth.drawable import Drawable
from pyth.globals import *
from ctypes import c_float

class Mine(Collidable, Drawable):
  def __init__(self, x, y, proximity_threshold, engine):
    Collidable.__init__(self, x, y, proximity_threshold)
    Drawable.__init__(self, engine)    
    self.proximity_threshold = proximity_threshold
    self.img = SPRITE_MINE

  def PerformCollisionAction(self, pawn):
    self.engine.play_sound(1) # Mine pickup  
    
  def Draw(self, z_dist):
    self.engine.draw_sprite(c_float(self.x_position), c_float(self.y_position), c_float(z_dist), self.img)

  #Payne325: For the time being, mines are just collected and do nothing.
  #I guess this class is actually, DeactivatedMine...
  #def Activate(self, pawn):
    #pawn.TakeImmediateDamage(self.damage)
  
