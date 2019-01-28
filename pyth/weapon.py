from pyth.globals import *

class Weapon():
  def __init__(self, damage, hit_distance, img):
    self.damage = damage
    self.hit_distance = hit_distance
    self.img = img

  def GetImg(self):
    return self.img

  def GetDamage(self):
    return self.damage

  def GetHitDistance(self):
    return self.hit_distance

class Gun(Weapon):
  def __init__(self):
    Weapon.__init__(self, 5, 50, -1)#FISTS_SPRITE_INDEX) #Payne325: Need to implement draws for weapons.

class Fists(Weapon):
  def __init__(self):
    Weapon.__init__(self, 1, 1, -1) #FISTS_SPRITE_INDEX)

'''
class CricketBat(Weapon):
  def __init__(self):
    Weapon.__init__(self, 2, 2, CRICKET_BAT_SPRITE_INDEX)

class KnuckleDuster(Weapon):
  def __init__(self):
    Weapon.__init__(self, 4, 1, KNUCKLE_DUSTER_SPRITE_INDEX)

class Sword(Weapon):
  def __init__(self):
    Weapon.__init__(self, 5, 2, SWORD_SPRITE_INDEX)
'''
