from collidable import Collidable

class Trap(Collidable):
  def __init__(self, x, y, proximity_threshold):
    Collidable.__init__(self, x, y, proximity_threshold)
    self.proximity_threshold = proximity_threshold

  def Activate(self, pawn):
    pawn.TakeImmediateDamage(self.damage)
    
if __name__ == "__main__":
  print("Tests the Trap class")

