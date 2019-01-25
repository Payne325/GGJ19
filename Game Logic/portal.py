from collidable import Collidable
from pawn import Pawn

class Portal(Collidable):
  def __init__(self, x_position, y_position, x_target, y_target):

    Collidable.__init__(x_position, y_position, 1)

    self.x_target = x_target
    self.y_target = y_target

  def Transport(self, pawn):
    pawn.Relocate(x_target, y_target)

