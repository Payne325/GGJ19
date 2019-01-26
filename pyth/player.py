from pyth.pawn import Pawn
from pyth.drawable import Drawable
from ctypes import cdll, c_float
import math

class Player(Pawn, Drawable):
  def __init__(self, health, x_position, y_position, x_orientation, y_orientation, weapon, resource, speed):
    Pawn.__init__(self, health, x_position, y_position, x_orientation, y_orientation, weapon, speed)
    Drawable.__init__(self)
    self.resource = resource
    self.rotOff = 0.004

  def HandleKeys(self, dt, engine, enemies):
    if engine.get_key(0):
        self.MoveForward(dt)

    if engine.get_key(1):
        self.MoveLeft(dt)

    if engine.get_key(2):
        self.MoveBackward(dt)

    if engine.get_key(3):
        self.MoveRight(dt)

    if engine.get_key(6):
        self.Attack(enemies)

    if engine.get_key(4):
        self.RotateLeft(dt)

    if engine.get_key(5):
        self.RotateRight(dt)

  def MoveForward(self, dt):
    ori = self.GetOrientationAngle()
    self.x_velocity += (math.cos(ori) * self.speed) * dt
    self.y_velocity += -math.sin(ori) * self.speed * dt

  def MoveBackward(self, dt):
    ori = self.GetOrientationAngle()
    self.x_velocity += math.cos(ori) * -self.speed * dt
    self.y_velocity += -math.sin(ori) * -self.speed * dt

  def MoveLeft(self, dt):
    ori = self.GetOrientationAngle() + (math.pi/2)
    self.x_velocity += math.cos(ori) * -self.speed * dt
    self.y_velocity += -math.sin(ori) * -self.speed * dt

  def MoveRight(self, dt):
    ori = self.GetOrientationAngle() + (math.pi/2)
    self.x_velocity += math.cos(ori) * self.speed * dt
    self.y_velocity += -math.sin(ori) * self.speed * dt

  def RotateLeft(self, dt):
    ori = self.GetOrientationAngle() - self.rotOff * dt
    self.x_orientation = math.cos(ori)
    self.y_orientation = -math.sin(ori)

  def RotateRight(self, dt):
    ori = self.GetOrientationAngle() + self.rotOff * dt
    self.x_orientation = math.cos(ori)
    self.y_orientation = -math.sin(ori)

  def Draw(self, z_dist, engine):
    pass
    #engine.draw_sprite(self.x_position, self.y_position, 0, self.weapon.GetImg())
