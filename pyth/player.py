from pyth.pawn import Pawn
from pyth.drawable import Drawable
import math

class Player(Pawn, Drawable):
  def __init__(self, health, x_position, y_position, x_orientation, y_orientation, weapon, resource, speed):
    Pawn.__init__(self, health, x_position, y_position, x_orientation, y_orientation, weapon, speed)
    Drawable.__init__(self)
    self.resource = resource
    self.rotOff = 0.05

  def HandleKeys(self, engine, enemies):
    if engine.get_key(0):
        self.MoveForward()

    if engine.get_key(1):
        self.MoveLeft()

    if engine.get_key(2):
        self.MoveBackward()

    if engine.get_key(3):
        self.MoveRight()

    if engine.get_key(6):
        self.Attack(enemies)

    if engine.get_key(4):
        self.RotateLeft()

    if engine.get_key(5):
        self.RotateRight()

  def MoveForward(self):
    ori = self.GetOrientationAngle()
    self.x_position += math.cos(ori) * self.speed
    self.y_position += -math.sin(ori) * self.speed

  def MoveBackward(self):
    ori = self.GetOrientationAngle()
    self.x_position += math.cos(ori) * -self.speed
    self.y_position += -math.sin(ori) * -self.speed

  def MoveLeft(self):
    ori = self.GetOrientationAngle() + (math.pi/2)
    self.x_position += math.cos(ori) * -self.speed
    self.y_position += -math.sin(ori) * -self.speed

  def MoveRight(self):
    ori = self.GetOrientationAngle() + (math.pi/2)
    self.x_position += math.cos(ori) * self.speed
    self.y_position += -math.sin(ori) * self.speed

  def RotateLeft(self):
    ori = self.GetOrientationAngle() - self.rotOff
    self.x_orientation = math.cos(ori)
    self.y_orientation = -math.sin(ori)

  def RotateRight(self):
    ori = self.GetOrientationAngle() + self.rotOff
    self.x_orientation = math.cos(ori)
    self.y_orientation = -math.sin(ori)

  def Draw(self, z_dist, engine):
    engine.draw_sprite(self.x_position, self.y_position, 0, self.weapon.GetImg())    

if __name__ == "__main__":
  Print("Test Player Class")



