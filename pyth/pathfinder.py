import sys, random
from pyth.pawn import Pawn

class Pathfinder:
  def __init__(self, engine):
    self.engine = engine

  def GetNewVelocity(self, start_x, start_y, target_x, target_y):
    startNode = Node(int(start_x), int(start_y), 0, False, None)
    openList = [startNode]
    closedList = []

    jitterator = 0
    while(len(openList) != 0):
      jitterator += 1
      lowestCost = sys.maxsize
      examinedNode = Node(-1,-1,-1, False, None)

      #print("Open: " + str(openList))
      #print("Closed: " + str(closedList))

      for node in openList:
        if node.GetCost() < lowestCost:
          lowestCost = node.GetCost()
          examinedNode = node

      #if that node is our target then path complete
      if (examinedNode.GetPosition()[0] == int(target_x) and examinedNode.GetPosition()[1] == int(target_y)) or jitterator >= 30:
        #RETURN PATH

        path = [examinedNode]
        flag = True

        pathNode = examinedNode
        while(pathNode.GetPrevNode() != None):
          path.append(pathNode.GetPrevNode())
          pathNode = pathNode.GetPrevNode()

        pathSize = len(path)
        firstNode = path[pathSize-1]
        secondNode = path[pathSize-2]

        x = secondNode.GetPosition()[0] + 0.5 -start_x
        y = secondNode.GetPosition()[1] + 0.5 -start_y

        if secondNode.GetPosition() == firstNode.GetPosition():
            return (random.randint(-10, 10), random.randint(-10, 10))

        return [x, y]
      else:
        closedList.append(examinedNode)

        x = examinedNode.GetPosition()[0]
        y = examinedNode.GetPosition()[1]

        dirs = [
            ( 0,  1),
            ( 0, -1),
            ( 1,  0),
            (-1,  0),
        ]
        for d in dirs:
            i = int(x) + d[0]
            j = int(y) + d[1]

            found = False
            isObsticle = self.engine.get_cell_kind(i, j) > 0
            cost = sys.maxsize if isObsticle else max(abs(x - target_x), abs(y - target_y))

            adjacentNode = Node(i, j, cost, isObsticle, examinedNode)

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

        openList.remove(examinedNode)
    return (random.randint(-10, 10), random.randint(-10, 10))

class Node:
  def __init__(self, x, y, cost, isObsticle, prevNode):
    self.position = (x,y)
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
