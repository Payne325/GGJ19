from pyth.collidable import Collidable
from pyth.drawable import Drawable
from pyth.globals import *

class HealthPack(Collidable, Drawable):
  def __init__(self, x, y, proximity_threshold, engine):
    Collidable.__init__(self, x, y, proximity_threshold)
    Drawable.__init__(self, engine)
    self.proximity_threshold = proximity_threshold
    self.img = SPRITE_HEALTH

  def PerformCollisionAction(self, pawn):
    self.engine.play_sound(1)
    pawn.health = min(20, pawn.health + 1)
