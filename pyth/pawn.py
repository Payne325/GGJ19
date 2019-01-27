import math
from ctypes import cdll, c_float

class Pawn:
  def __init__(self, health, x_position, y_position, x_orientation, y_orientation, weapon, speed):
    self.health = health
    self.x_position = x_position
    self.y_position = y_position
    self.x_orientation = x_orientation
    self.y_orientation = y_orientation
    self.weapon = weapon
    self.attack_cooldown = 10
    self.speed = speed
    self.x_velocity = 0.0
    self.y_velocity = 0.0

  def Tick(self, engine, dt):
    vel_len = math.sqrt(self.x_velocity ** 2.0 + self.y_velocity ** 2.0)
    for i in range(int(dt ** 0.4) + 2):
        self.x_velocity *= 0.85
        self.y_velocity *= 0.85
    self.attack_cooldown += 1

    def would_collide(this, engine, x, y):
        dirs = [
            (-0.25, -0.25),
            (-0.25,  0.25),
            ( 0.25, -0.25),
            ( 0.25,  0.25)
        ]
        for d in dirs:
            if engine.get_cell_kind(int(this.x_position + x + d[0]), int(this.y_position + y + d[1])) != 0:
                return True
        return False

    if would_collide(self, engine, self.x_velocity, self.y_velocity):
        dist = 0.0
        while dist < 1.0:
            if not would_collide(self, engine, self.x_velocity * 0.05, 0.0):
                self.x_position += self.x_velocity * 0.05
            if not would_collide(self, engine, 0.0, self.y_velocity * 0.05):
                self.y_position += self.y_velocity * 0.05
            dist += 0.05
    else:
        self.x_position += self.x_velocity
        self.y_position += self.y_velocity



  def GetXPosition(self):
    return self.x_position

  def GetYPosition(self):
    return self.y_position

  def GetOrientationAngle(self):
    return math.atan2(-self.y_orientation, self.x_orientation)

  def Relocate(self, x, y):
    self.x_position = x
    self.y_position = y

  def TakeImmediateDamage(self, damage):
    self.health = self.health - damage

  def Intersects(self, ray_length, ray_x_point, ray_y_point, ray_x_direction, ray_y_direction):
    #determines if the specified ray intersects this object's position

    #If current position lies within two points defined by the ray
    #then we are hit
    rayPointX1 = ray_x_point
    rayPointX2 = ray_x_point + (ray_x_direction * ray_length)

    rayPointY1 = ray_y_point
    rayPointY2 = ray_y_point + (ray_y_direction * ray_length)

    dxc = self.x_position - rayPointX1
    dyc = self.y_position - rayPointY1

    dxl = rayPointX2 - rayPointX1
    dyl = rayPointY2 - rayPointY1

    cross = dxc * dyl - dyc * dxl

    return cross == 0

  def hit_other(self, engine, other):
    def norm(x, y):
        leng = math.sqrt(x * x + y * y)
        return (
            x / leng,
            y / leng
        )

    def dot(a, b):
        return a[0] * b[0] + a[1] * b[1]

    to_other = (
        other.x_position - self.x_position,
        other.y_position - self.y_position
    )
    to_other_leng = math.sqrt(to_other[0] * to_other[0] + to_other[1] * to_other[1])

    dot_result = dot(
        (to_other[0] / to_other_leng, to_other[1] / to_other_leng),
        (self.x_orientation, self.y_orientation)
    )

    ray_dist = float(engine.cast_ray(
        c_float(self.x_position),
        c_float(self.y_position),
        c_float(to_other[0] / to_other_leng),
        c_float(to_other[1] / to_other_leng),
        c_float(0.3) # Minimum obstacle height
    )) / 100.0 # cast_ray produces 100x the distance because hur dur C FFI

    #print(ray_dist)
    #print(to_other_leng)
    if dot_result > math.pow(0.99, 1.0 / to_other_leng) and ray_dist > to_other_leng - 0.1: # <-- Account for stuck in walls
        return (True, to_other_leng)
    else:
        return (False, ray_dist)

  def Attack(self, engine, pawns):
    if self.attack_cooldown < 15:
        return
    else:
        self.attack_cooldown = 0

    #hit scan fire.
    #fires a ray of specified size when attack is called
    ray_length = self.weapon.GetHitDistance()
    ray_x_direction = self.x_orientation
    ray_y_direction = self.y_orientation
    ray_x_point = self.x_position
    ray_y_point = self.y_position

    closest = None
    closest_dist = 1000.0
    for pawn in pawns:
      #hit = pawn.Intersects(ray_length, ray_x_point, ray_y_point, ray_x_direction, ray_y_direction)
      hit = self.hit_other(engine, pawn)
      if hit[0] == True and hit[1] <= self.weapon.GetHitDistance():
        #print("HIT!")
        if hit[1] < closest_dist:
            closest = pawn
            closest_dist = hit[1]

    if closest != None:
        print("HIT!")
        engine.play_sound(2) # Attack sound
        closest.TakeImmediateDamage(self.weapon.GetDamage())
