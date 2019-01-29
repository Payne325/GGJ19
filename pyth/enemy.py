from pyth.pawn import Pawn
from pyth.state_machine import State_Machine
from pyth.pathfinder import Pathfinder
from pyth.drawable import Drawable
from pyth.globals import *
from ctypes import cdll, c_float
import math
import random

class Enemy(Pawn, Drawable):
  def __init__(self, health, x_position, y_position, x_orientation, y_orientation, weapon, speed, engine):
    Pawn.__init__(self, health, x_position, y_position, x_orientation, y_orientation, weapon, speed, engine)
    Drawable.__init__(self, engine)
    #self.state_machine = State_Machine(sightRange)
    self.pathfinder = Pathfinder(engine)
    self.img = SPRITE_ZOMBIE

    self.prev_x = -1
    self.prev_y = -1
    self.tgt_velocity = (0, 0)

    def TakeImmediateDamage(self, damage):
      Pawn.TakeImmediateDamage(self, damage)
      self.engine.play_sound(14)

  def Update(self, targetPawn):
    def DoAttack(this, targetPawn):
      playerPos = [targetPawn.GetXPosition(), targetPawn.GetYPosition()]
      enemyPos = [this.GetXPosition(), this.GetYPosition()]

      distance = math.sqrt(
                ((playerPos[0] - enemyPos[0]) * (playerPos[0] - enemyPos[0])) +
                ((playerPos[1] - enemyPos[1]) * (playerPos[1] - enemyPos[1])))

      if (distance < 4):
        this.x_orientation = (playerPos[0] - enemyPos[0]) / distance
        this.y_orientation = (playerPos[1] - enemyPos[1]) / distance
        #print("\nOrientation: " + self.x_orientation + " " + self.y_orientation)
        this.Attack([targetPawn])

    if (self.prev_x != int(self.x_position) or self.prev_y != int(self.y_position)) or random.randint(0, 100) == 0:
      target_x = targetPawn.GetXPosition()
      target_y = targetPawn.GetYPosition()

      new_velocity = self.pathfinder.GetNewVelocity(self.x_position, self.y_position, target_x, target_y)

      #normalise velocity and set x & y orientation
      magnitude = max(math.sqrt((self.x_velocity*self.x_velocity) + (self.y_velocity*self.y_velocity)), 0.01)
      self.x_orientation = self.x_velocity/magnitude
      self.y_orientation = self.y_velocity/magnitude

      new_magnitude = max(math.sqrt((new_velocity[0]*new_velocity[0]) + (new_velocity[1]*new_velocity[1])), 0.01)
      self.tgt_velocity = (new_velocity[0] / new_magnitude, new_velocity[1] / new_magnitude)

      self.prev_x = int(self.x_position)
      self.prev_y = int(self.y_position)

    self.x_velocity += self.tgt_velocity[0] * self.speed
    self.y_velocity += self.tgt_velocity[1] * self.speed

    DoAttack(self, targetPawn)

  def Draw(self, player_one):
    rx = player_one.x_position - self.x_position
    ry = player_one.y_position - self.y_position
    dist = math.sqrt(rx * rx + ry * ry)
    self.engine.draw_sprite(c_float(self.x_position), c_float(self.y_position), c_float(dist), self.img)
