class Collidable:
  def __init__(self, x_position, y_position):
    self.x_position = x_position
    self.y_position = y_position

  def HasCollidedWith(self, pawn):
    x_range = abs(pawn.GetXPosition() - self.x_position)
    y_range = abs(pawn.GetYPosition() - self.y_position)
    
    if(x_range <= self.proximity_threshold):
      return True

    elif(y_range <= self.proximity_threshold):
      return True
    
    else:
      return False
