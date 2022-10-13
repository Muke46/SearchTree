import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons, Button, TextBox

from SearchTree import Node, Tree
from math import dist



class PathFinding(Tree):
    def __init__(self, rootNode=(0,0), path='', walkableColor = [1., 1., 1., 1.], heuristic = 'LineOfSight'):
        super().__init__(rootNode)

        self.path=path
        #convert to int 3-tuple
        self.map = mpimg.imread(path)
        self.map=self.map[:,:,0:3]
        self.map=self.map*255
        self.map = self.map.astype(int)

        self.vismap = self.map.copy()

        self.walkableColor = walkableColor

        self.heuristic = heuristic # LineOfSight or Manhattan

    
    def updateVisualization(self, expandedNode):
        pass

    def expandNode(self, node):
        if self.showVisualization:
            self.vismap[node.data[0]][node.data[1]] = [255, 0, 0]
        childList=[]
        y, x = node.data
        #up
        if y>0 and (self.map[y-1][x]==self.walkableColor).all():
            newNode = Node((y-1,x))
            newNode.parent=node
            childList.append(newNode)
        #down
        if y<self.map.shape[0]-1 and (self.map[y+1][x]==self.walkableColor).all():
            newNode = Node((y+1,x))
            newNode.parent=node
            childList.append(newNode)
        #left
        if x>0 and (self.map[y][x-1]==self.walkableColor).all():
            newNode = Node((y,x-1))
            newNode.parent=node
            childList.append(newNode)
        #right
        if x<self.map.shape[1]-1 and (self.map[y][x+1]==self.walkableColor).all():
            newNode = Node((y,x+1))
            newNode.parent=node
            childList.append(newNode)
        # for ch in childList:
        #     self.vismap[ch.data[0]][ch.data[1]] = [0., 0., 1., 1.]
        return childList

    def getActionCost(self, beginNode, endNode):
        return 1
    def getHeuristic(self, node):
        if self.heuristic == 'LineOfSight':return (dist(self.goal,node.data))
        if self.heuristic == 'Manhattan':  return abs(self.goal[0]-node.data[0])+abs(self.goal[1]-node.data[1])


# test = PathFinding(rootNode=(50,50), path="Resources\home_map.png")

# path = test.find(goal=(154,198), print_steps=False, stepByStep=False, showVisualization=False, avoidRepeat="Tree", searchtype="A*")
# print(path)
#test.GUI()