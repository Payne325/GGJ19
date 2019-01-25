class Trap:
  def __init__(self, x, y, proximity_threshold):
    self.x_pos = x
    self.y_pos = y
    self.proximity_threshold = proximity_threshold

  def HasCollidedWith(self, x, y):
    x_range = abs(x - self.x_pos)
    y_range = abs(y - self.y_pos)
    
    if(x_range <= self.proximity_threshold):
      return True

    elif(y_range <= self.proximity_threshold):
      return True
    
    else:
      return False


if __name__ == "__main__":
  print("Tests the Trap class")

  mine = Trap(16, 16, 2)

  if(mine.HasCollidedWith(9, 9)):
    print("At (9,9), BOOM!")
  else:
    print("At (9,9), No Boom Boom")

  if(mine.HasCollidedWith(15, 15)):
    print("At (15, 15), BOOM!")
  else:
    print("At (15,15), No Boom Boom")
