from pyth.player import Player
from pyth.enemy import Enemy
from pyth.weapon import *
import math, random

class Factory():
  def CreateEnemy(engine, x, y, mult):
    return Enemy(
        health=math.trunc(3*mult),
        x_position=x,
        y_position=y,
        x_orientation=-1,
        y_orientation=-1,
        weapon=Fists(),
        speed=0.014*mult, #speed=random.randint(1, 4) * 0.01,
        engine=engine)

  def CreatePlayer(engine):
    return Player(
                health=10,
                x_position=18.5,
                y_position=18.5,
                x_orientation=1.0,
                y_orientation=0.0,
                weapon=Gun(),
                resource=50,
				        speed=0.007,
                engine=engine)
