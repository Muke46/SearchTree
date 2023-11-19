import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons, Button, TextBox

from SearchTree import Node, Tree
from math import dist

class SolitarioSearchTree(Tree):
    def __init__(self):
        self.emptyColor = [0, 0, 0]
        self.wallColor = [0, 255, 0]
        self.pegColor = [255, 255, 255]

        rootNode = mpimg.imread("C:\Files\SearchTree\Resources\Solitario_UK.png")
        rootNode = rootNode[:,:,0:3]
        rootNode = rootNode*255
        rootNode = rootNode.astype(int)

        super().__init__(rootNode)

        self.goal = mpimg.imread("C:\Files\SearchTree\Resources\goal.png")
        self.goal = self.goal[:,:,0:3]
        self.goal = self.goal*255
        self.goal = self.goal.astype(int)
    
    def updateVisualization(self, expandedNode):
        pass

    def expandNode(self, node):

        childList=[]

        for x in range(len(node.data[0])):
            for y in range(len(node.data[0])):
                if(node.data[x][y]==self.pegColor):
                    #up
                    if (x-2)>0 and node.data[x-2][y] == self.emptyColor:
                        data = node.data
                        data[x-2][y] = self.pegColor
                        data[x-1][y] = self.emptyColor
                        newNode = Node(data)
                        newNode.parent=node
                        childList.append(newNode)

        return childList

    def getActionCost(self, beginNode, endNode):
        return 1
    def getHeuristic(self, node):
        pass


test = SolitarioSearchTree()
path = test.find()

# path = test.find(goal=(154,198), print_steps=False, stepByStep=False, showVisualization=False, avoidRepeat="Tree", searchtype="A*")
# print(path)
#test.GUI()