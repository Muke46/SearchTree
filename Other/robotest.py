from logging import root
from turtle import goto, up
from SearchTree import Node, Tree
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math

from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication


class Roborock(Tree):
    def __init__(self, rootNode, imgMap):
        super().__init__(rootNode)
        self.map = mpimg.imread(imgMap)
        self.vismap = mpimg.imread(imgMap) #used for visualization
        self.vismap[self.root.data[0]][self.root.data[1]] = [0., 1., 0., 1.]

        self.wallColor = [0., 0., 0., 1.]
        self.walkableColor = [1., 1., 1., 1.]

        _, ax = plt.subplots(figsize=(7, 8))
        self.imgplot = ax.imshow(self.map)


    def showVisualization(self):
        #goal
        if self.goal!=None:
            self.vismap[self.goal[0]][self.goal[1]] = [0., 0., 1., 1.]

        #tree
        self.imgplot.set_data(self.vismap)
        plt.pause(0.01)

    def expandNode(self, node):
        if self.showVisualization:
            self.vismap[node.data[0]][node.data[1]] = [1., 0., 0., 1.]
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

        return childList

    def getActionCost(self, beginNode, endNode):
        return 1
    def getHeuristic(self, node):
        #manhattan  distance
        #return abs(self.goal[0]-node.data[0])+abs(self.goal[1]-node.data[1])
        return (math.dist(self.goal,node.data))


test = Roborock(rootNode=(42,42),imgMap="D:\Git\SearchTree\Resources\home_map.png")
test.showVisualization()
#input("Press ENTER to start")
path = test.find(goal=(154,198), print_steps=False, stepByStep=False, showVisualization=True, avoidRepeat="Tree", searchtype="A*")
print(path)
plt.show()
'''

a = Node((16,2))
#test.map[a.data[0]][a.data[1]] = [1., 0., 0., 1.]

test.expandNode(a)
test.print()

plt.show()
#input("Press Enter to continue...")

'''