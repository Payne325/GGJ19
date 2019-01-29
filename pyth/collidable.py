from pyth.pawn import Pawn
import math

class Collidable:
  def __init__(self, x_position, y_position, proximity_threshold):
    self.x_position = x_position
    self.y_position = y_position
    self.proximity_threshold = proximity_threshold

  def PerformCollisionAction(self, pawn):
    print("This is the 'Collidable' abstract class you levitating tea spoon!")
    sys.exit()

  def HasCollidedWith(self, pawn):
    rx = abs(pawn.GetXPosition() - self.x_position)
    ry = abs(pawn.GetYPosition() - self.y_position)

    dist = math.sqrt(rx * rx + ry * ry)
    
    if(dist <= self.proximity_threshold):
      return True    
    else:
      return False
