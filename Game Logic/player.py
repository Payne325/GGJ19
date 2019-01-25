from pawn import Pawn

class Player(Pawn):
  def __init__(self, health, x_position, y_position, x_orientation, y_orientation, weapon, resource):
    Pawn.__init__(health, x_position, y_position, x_orientation, y_orientation, weapon)
    self.resource = resource

  def Move(self):
    new_x_position = self.x_position + (self.x_orientation * self.speed)
    new_y_position = self.y_position + (self.y_orientation * self.speed)

  def Rotate(self, rotationVal):
    #perform rotation

if __name__ == "__main__":
  Print("Test Player Class")



