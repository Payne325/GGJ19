class Pawn:
  def __init__(self, health, x_position, y_position, x_orientation, y_orientation, weapon, speed):
    self.health = health
    self.x_position = x_position
    self.y_position = y_position
    self.x_orientation = x_orientation
    self.y_orientation = y_orientation
    self.weapon = weapon
    self.speed = speed

  def GetXPosition(self):
    return self.x_position

  def GetYPosition(self):
    return self.y_position

  def Relocate(self, x, y):
    self.x_position = x
    self.y_position = y

  def TakeImmediateDamage(self, damage):
    self.health = self.health - damage

  def TakeHit(self, ray_length, ray_x_point, ray_y_point, ray_x_direction, ray_y_direction, damage):
    #if the specified ray intersects this object's position)
    #take damage

    #If current position lies within two points defined by the ray
    #then we have taken a hit
    rayPointX1 = ray_x_point
    rayPointX2 = ray_x_point + (ray_x_direction * ray_length)

    rayPointY1 = ray_y_point
    rayPointY2 = ray_y_point + (ray_y_direction * ray_length)

    dxc = self.x_position - rayPointX1
    dyx = self.y_position - rayPointY1

    dxl = rayPointX2 - rayPointX1
    dyl = rayPointY2 - rayPointY1

    cross = dxc * dyl - dyc * dxl

    if cross == 0:
      TakeImmediateDamage(damage)

  def Attack(self, pawns):
    #hit scan fire.
    #fires a ray of specified size when attack is called
    ray_length = self.weapon.GetHitDistance()
    ray_x_direction = self.x_orientation
    ray_y_direction = self.y_orientation
    ray_x_point = self.x_position
    ray_y_point = self.y_position
    damage = self.weapon.GetDamage()

    for pawn in pawns:
      enemy.TakeHit(ray_length, ray_x_point, ray_y_point, ray_x_direction, ray_y_direction, damage)
