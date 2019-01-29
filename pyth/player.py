from pyth.pawn import Pawn
from pyth.drawable import Drawable
from ctypes import cdll, c_float
import math

class Player(Pawn, Drawable):
  def __init__(self, health, x_position, y_position, x_orientation, y_orientation, weapon, resource, speed, engine):
    Pawn.__init__(self, health, x_position, y_position, x_orientation, y_orientation, weapon, speed, engine)
    Drawable.__init__(self, engine)
    self.resource = resource
    self.rotOff = 0.003
    self.mine_count = 0
    self.moveCounter = 0
    self.sfCooldown = 15

  def Tick(self, dt):
    self.sfCooldown += 1
    Pawn.Tick(self, dt)

  def TakeImmediateDamage(self, damage):
    Pawn.TakeImmediateDamage(self, damage)
    self.engine.play_sound(11)

  def PlayMoveSF(self):
    if self.sfCooldown < 15:
      return
    
    self.sfCooldown = 0

    self.engine.play_sound(self.moveCounter + 4)
    if self.moveCounter == 3:
      self.moveCounter = 0
    else:
      self.moveCounter += 1

  def HandleKeys(self, dt, enemies):
    if self.engine.get_key(0):
        multi = 0.3 if self.engine.get_key(7) else 1.5
        self.MoveForward(dt, multi)
        self.PlayMoveSF()

    if self.engine.get_key(1):
        multi = 0.3 if self.engine.get_key(7) else 0.8
        self.MoveLeft(dt, multi)
        self.PlayMoveSF()

    if self.engine.get_key(2):
        multi = 0.3 if self.engine.get_key(7) else 1.5
        self.MoveBackward(dt, multi)
        self.PlayMoveSF()

    if self.engine.get_key(3):
        multi = 0.3 if self.engine.get_key(7) else 0.8
        self.MoveRight(dt, multi)
        self.PlayMoveSF()

    if self.engine.get_key(6):
        self.Attack(enemies)
        if self.attack_cooldown == 0:
            self.engine.play_sound(0)

    if self.engine.get_key(4):
        multi = 0.2 if self.engine.get_key(7) else 1.0
        self.RotateLeft(dt, multi)

    if self.engine.get_key(5):
        multi = 0.2 if self.engine.get_key(7) else 1.0
        self.RotateRight(dt, multi)

  def MoveForward(self, dt, multi):
    ori = self.GetOrientationAngle()
    self.x_velocity += (math.cos(ori) * self.speed) * dt * multi
    self.y_velocity += -math.sin(ori) * self.speed * dt * multi

  def MoveBackward(self, dt, multi):
    ori = self.GetOrientationAngle()
    self.x_velocity += math.cos(ori) * -self.speed * dt * multi
    self.y_velocity += -math.sin(ori) * -self.speed * dt * multi

  def MoveLeft(self, dt, multi):
    ori = self.GetOrientationAngle() + (math.pi/2)
    self.x_velocity += math.cos(ori) * -self.speed * dt * multi
    self.y_velocity += -math.sin(ori) * -self.speed * dt * multi

  def MoveRight(self, dt, multi):
    ori = self.GetOrientationAngle() + (math.pi/2)
    self.x_velocity += math.cos(ori) * self.speed * dt * multi
    self.y_velocity += -math.sin(ori) * self.speed * dt * multi

  def RotateLeft(self, dt, multi):
    ori = self.GetOrientationAngle() - self.rotOff * dt * multi
    self.x_orientation = math.cos(ori)
    self.y_orientation = -math.sin(ori)

  def RotateRight(self, dt, multi):
    ori = self.GetOrientationAngle() + self.rotOff * dt * multi
    self.x_orientation = math.cos(ori)
    self.y_orientation = -math.sin(ori)

  def Draw(self, player):
    pass    
    #engine.draw_sprite(self.x_position, self.y_position, 0, self.weapon.GetImg())
