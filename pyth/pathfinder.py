import sys
from pyth.pawn import Pawn

class Pathfinder:
  def __init__(self, engine, sight):
    self.engine = engine
    self.sight = sight

  def GeneratePath(self, start_x, start_y, target_x, target_y):
    halfSight = sight/2
    max_x = start_x + halfSight
    max_y = start_y + halfSight
    min_x = start_x - halfSight
    min_y = start_y - halfSight

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

        return path

      else:
        closedList.append(examinedNode)
        adjacentNodes = []

        x = examinedNode.GetXPosition()
        y = examinedNode.GetYPosition()

        for i in range(x-1, x+1):
          found = False
          if i < min_x or i > max_x:
            continue;

          for j in range(y-1, y+1):
            if j < min_y or j > max_y:
              continue;

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
