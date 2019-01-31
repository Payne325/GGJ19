from pyth.collidable import Collidable
from pyth.drawable import Drawable
from pyth.globals import *

class Mine(Collidable, Drawable):
  def __init__(self, x, y, proximity_threshold, engine):
    Collidable.__init__(self, x, y, proximity_threshold)
    Drawable.__init__(self, engine)    
    self.proximity_threshold = proximity_threshold
    self.img = SPRITE_MINE

  def PerformCollisionAction(self, pawn):
    self.engine.play_sound(1) # Mine pickup
    pawn.mine_count += 1
    
  #Payne325: For the time being, mines are just collected and do nothing.
  #I guess this class is actually, DeactivatedMine...
  #def Activate(self, pawn):
    #pawn.TakeImmediateDamage(self.damage)
  
