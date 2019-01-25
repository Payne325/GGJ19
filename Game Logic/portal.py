from collidable import Collidable

class Portal(Collidable):
  def __init__(self, x_position, y_position, x_target, y_target):

    Collidable.__init__(x_position, y_position)

    self.x_target = x_target
    self.y_target = y_target

