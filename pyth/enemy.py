from pyth.pawn import Pawn
from pyth.state_machine import State_Machine
from pyth.pathfinder import Pathfinder
from pyth.drawable import Drawable

class Enemy(Pawn, Drawable):
  def __init__(self, health, x_position, y_position, x_orientation, y_orientation, weapon, sightRange, engine):
    Pawn.__init__(health, x_position, y_position, x_orientation, y_orientation, weapon)
    Drawable.__init__(self)
    self.sightRange = sightRange
    #self.state_machine = State_Machine(sightRange)
    self.pathfinder = Pathfinder(engine, sightRange)
    self.img = None

  def Update(self, targetPawn):
    #self.state_machine.Update(self.x_position, self.y_position, targetPawn)

    target_x = targetPawn.GetXPosition()
    target_y = targetPawn.GetYPosition()

    path = self.pathfinder.GeneratePath(self.x_position, self.y_position, target_x, target_y)

    

  def Move(self):
    new_x_position = self.x_position + (self.x_orientation * self.speed)
    new_y_position = self.y_position + (self.y_orientation * self.speed)

  def Rotate(self, rotationVal):
    pass
	  #perform rotation

  def Draw(self, z_dist, engine):
    engine.draw_sprite(self.x_position, self.y_position, z_dist, self.img) 
