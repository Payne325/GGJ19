class Weapon:
  def __init__(self, damage, hit_distance):
    self.damage = damage
    self.hit_distance = hit_distance

  def GetDamage(self):
    return self.damage

  def GetHitDistance(self):
    return self.hit_distance

