from collidable import Collidable

class Trap(Collidable):
  def __init__(self, x, y, proximity_threshold):
    Collidable.__init__(self, x, y)
    self.proximity_threshold = proximity_threshold

if __name__ == "__main__":
  print("Tests the Trap class")

  mine = Trap(16, 16, 2)
