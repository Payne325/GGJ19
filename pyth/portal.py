from pyth.collidable import Collidable
from pyth.pawn import Pawn
from pyth.drawable import Drawable
from pyth.globals import *

class Portal(Collidable, Drawable):
  def __init__(self, x_position, y_position, x_target, y_target, engine):

    Collidable.__init__(self, x_position, y_position, 1)
    Drawable.__init__(self, engine)
    self.x_target = x_target
    self.y_target = y_target
    self.img = PORTAL_SPRITE_INDEX

  def Transport(self, pawn):
    pawn.Relocate(x_target, y_target)

  def Draw(self, z_dist):
    self.engine.draw_sprite(self.x_position, self.y_position, z_dist, self.img)
