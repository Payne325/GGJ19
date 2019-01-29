from ctypes import c_float
import sys, math

class Drawable:
  def __init__(self, engine):
    self.engine = engine
    self.dist = -1

  def Draw(self, player):
    rx = player.x_position - self.x_position
    ry = player.y_position - self.y_position
    dist = math.sqrt(rx * rx + ry * ry)
    self.engine.draw_sprite(c_float(self.x_position), c_float(self.y_position), c_float(dist), self.img)
