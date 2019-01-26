import sys
from pyth.pawn import Pawn

class Pathfinder:
  def __init__(self, engine):
    self.engine = engine

  def GetNewVelocity(self, start_x, start_y, target_x, target_y):
    startNode = Node(start_x, start_y, 0, False, None)
    openList = [startNode]
    closedList = []

    while(len(openList) != 0):
      lowestCost = sys.maxint
      examinedNode = Node(-1,-1,-1, False, None)

      for node in openList:
        if node.GetCost() < lowestCost:
          lowestCost = Node.GetCost()
          examinedNode = node

      #if that node is our target then path complete
      if node.GetPosition() == [target_x, target_y]:
        #RETURN PATH

        path = [node]
        flag = True

        pathNode = node
        while(pathNode.GetPrevNode() != null):
          path.append(pathNode.GetPrevNode())
          pathNode = pathNode.GetPrevNode()

        pathSize = len(path)
        firstNode = path[pathSize-1]
        secondNode = path[pathSize-2]

        x = secondNode.GetPosition()[0] -firstNode.GetPosition()[0] 
        y = secondNode.GetPosition()[1] -firstNode.GetPosition()[1]

        return [x, y]
      else:
        closedList.append(examinedNode)
        adjacentNodes = []

        x = examinedNode.GetXPosition()
        y = examinedNode.GetYPosition()

        for i in range(x-1, x+1):
          found = False

          for j in range(y-1, y+1):
            isObsticle = self.engine.get_cell_kind(i, j)
            cost = sys.maxint if isObsticle else 0

            adjacentNode = Node(i, j, cost, isObsticle == 0, examinedNode)

            for item in openList:
              if item.GetPosition() == adjacentNode.GetPosition():
                found = True

            for item in closedList:
              if item.GetPosition() == adjacentNode.GetPosition():
                found = True

            if adjacentNode.GetIsObsticle():
              found = True

          if found == False:
            openList.append(adjacentNode)

class Node:
  def __init__(self, x, y, cost, isObsticle, prevNode):
    self.position = [x,y]
    self.cost = cost
    self.isObsticle = isObsticle
    self.prevNode = prevNode

  def GetCost(self):
    return self.cost

  def GetPosition(self):
    return self.position

  def GetIsObsticle(self):
    return self.isObsticle

  def GetPrevNode(self):
    return self.prevNode
