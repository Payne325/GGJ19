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

class Fists(Weapon):
  def __init__(self):
    Weapon.__init__(self, 1, 1, None)

class CricketBat(Weapon):
  def __init__(self):
    Weapon.__init__(self, 2, 2, None)

class KnuckleDuster(Weapon):
  def __init__(self):
    Weapon.__init__(self, 4, 1, None)

class Sword(Weapon):
  def __init__(self):
    Weapon.__init__(self, 5, 2, None)
