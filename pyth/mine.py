from pyth.collidable import Collidable
from pyth.drawable import Drawable
from pyth.globals import *

class Mine(Collidable):
  def __init__(self, x, y, proximity_threshold, engine):
    Collidable.__init__(self, x, y, proximity_threshold)
    Drawable.__init__(self, engine)    
    self.proximity_threshold = proximity_threshold
    self.img = MINE_SPRITE_INDEX

  def Activate(self, pawn):
    pawn.TakeImmediateDamage(self.damage)
    
  def Draw(self, z_dist):
    self.engine.draw_sprite(self.x_position, self.y_position, z_dist, self.img)
