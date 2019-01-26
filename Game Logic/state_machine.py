class State_Machine:
  def __init__(self, sightRange):
    self.state = "Seek"
    self.x_target_location = 1
    self.y_target_location = 1
    self.sightRange

  def GetTargetXLocation(self):
    return self.x_target_location

  def GetTargetYLocation(self):
    return self.y_target_location

  def Update(self, current_x, current_y, targetPawn):
    
    if self.state == "Seek":
      foundPawn = InSightOfPawn(current_x, current_y, targetPawn)
      if foundPawn:
        self.State = "Destroy"
      else:
        #set target location to some sensible search value

    elif self.state == "Destroy":
      foundPawn = InSightOfPawn(current_x, current_y, targetPawn)
      if foundPawn:
        self.x_target_location = pawn.GetXPosition()
        self.y_target_location = pawn.GetYPosition()
      else:
        self.State = "Seek"
        #set target location to some sensible search value


    def InSightOfPawn(self, current_x, current_y, pawn):
      x_range = abs(pawn.GetXPosition() - current_x)
      y_range = abs(pawn.GetYPosition() - current_y)
    
      if(x_range <= self.sightRange):
        return True
      elif(y_range <= self.sightRange):
        return True
      else:
        return False
