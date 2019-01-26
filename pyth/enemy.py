from pyth.pawn import Pawn
from pyth.state_machine import State_Machine
from pyth.pathfinder import Pathfinder

class Enemy(Pawn):
  def __init__(self, health, x_position, y_position, x_orientation, y_orientation, weapon, sightRange, world):
    Pawn.__init__(health, x_position, y_position, x_orientation, y_orientation, weapon)
    self.sightRange = sightRange
    self.state_machine = State_Machine(sightRange)
    self.pathfinder = Pathfinder(world, sightRange)

  def Update(self, targetPawn):
    self.state_machine.Update(self.x_position, self.y_position, targetPawn)

    target_x = self.state_machine.GetTargetXLocation()
    target_y = self.state_machine.GetTargetYLocation()

    path = self.pathfinder.GeneratePath(self.x_position, self.y_position, target_x, target_y)

    #do some relevant rotation and movement.

  def Move(self):
    new_x_position = self.x_position + (self.x_orientation * self.speed)
    new_y_position = self.y_position + (self.y_orientation * self.speed)

  def Rotate(self, rotationVal):
    pass
	#perform rotation
