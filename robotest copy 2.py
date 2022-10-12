import matplotlib.image as mpimg
import time
import matplotlib.pyplot as plt
from threading import Thread, Event

from SearchTree import Node, Tree
import math
from matplotlib.widgets import RadioButtons
from matplotlib.widgets import Button

path = "D:\Git\SearchTree\Resources\home_map_exp3.png"

class PathFinding(Tree):
    def __init__(self, rootNode, path):
        super().__init__(rootNode)
        self.map = mpimg.imread(path)
        self.vismap = mpimg.imread(path)

        #self.wallColor = [0., 0., 0., 1.]
        self.walkableColor = [1., 1., 1., 1.]

        self.searchType = 'BFS'
        self.goal = None
        self.start = None

    def changeSearchType(self, label):
        self.searchType = label

    def GUI_find(self, event):
        if self.goal == None:
            return
        if self.start != None:
            self.root.data = self.start
        else:
            return
        print(self.start)
        print(self.goal)
        self.map = mpimg.imread(path)
        self.vismap = mpimg.imread(path)
        self.resetTree()
        path_found=self.find(goal=self.goal, print_steps=False, stepByStep=False, showVisualization=True, avoidRepeat="Tree", searchtype=self.searchType)
        for el in path_found:
            self.vismap[el[0]][el[1]] = [0., 1., 0., 1.]
        self.im.set_data(self.vismap)
        self.fig.canvas.draw_idle()
        plt.pause(1)
    
    def GUI_reset(self, event):
        print("Reset!")
        self.start = None
        self.goal = None
        self.map = mpimg.imread(path)
        self.vismap = mpimg.imread(path)
        self.resetTree()
        tmp=self.vismap.copy()
        if self.goal != None:
            tmp[self.goal[0]][self.goal[1]] = [0., 1., 0., 1.]
        if self.start != None:
            tmp[self.start[0]][self.start[1]] = [0., 0., 1., 1.]
        self.im.set_data(tmp)
        self.fig.canvas.draw_idle()
        plt.pause(1/10)

    def GUIonclick(self, event):
        if event.inaxes != self.ax: return
        if event.button==1:
            self.start = (int(event.ydata),int(event.xdata))
        if event.button==3:
            self.goal = (int(event.ydata),int(event.xdata))
        tmp=self.vismap.copy()
        if self.goal != None:
            tmp[self.goal[0]][self.goal[1]] = [0., 1., 0., 1.]
        if self.start != None:
            tmp[self.start[0]][self.start[1]] = [0., 0., 1., 1.]
        self.im.set_data(tmp)
        self.fig.canvas.draw_idle()
        plt.pause(1/10)

    def GUI(self):
        self.fig,self.ax = plt.subplots(1,1)
        self.im = self.ax.imshow(self.vismap)
        rax = self.fig.add_axes([0.05, 0.7, 0.15, 0.15])
        radio = RadioButtons(rax, ('BFS', 'DFS', 'A*'))
        radio.on_clicked(self.changeSearchType)
        rax2 = self.fig.add_axes([0.05, 0.3, 0.15, 0.15])
        button = Button(rax2, "Start!")
        button.on_clicked(self.GUI_find)
        rax3 = self.fig.add_axes([0.05, 0.1, 0.15, 0.15])
        button2 = Button(rax3, "Reset")
        button2.on_clicked(self.GUI_reset)
        cid = self.fig.canvas.mpl_connect('button_press_event', self.GUIonclick)
        plt.show()


    def showVisualization(self):
        self.vismap[self.root.data[0]][self.root.data[1]] = [0., 0., 1., 1.]
        self.vismap[self.goal[0]][self.goal[1]] = [0., 1., 0., 1.]
        self.im.set_data(self.vismap)
        self.fig.canvas.draw_idle()
        plt.pause(1/10)

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
        # for ch in childList:
        #     self.vismap[ch.data[0]][ch.data[1]] = [0., 0., 1., 1.]
        return childList

    def getActionCost(self, beginNode, endNode):
        return 1
    def getHeuristic(self, node):
        #Manhattan  distance
        #return abs(self.goal[0]-node.data[0])+abs(self.goal[1]-node.data[1])
        return (math.dist(self.goal,node.data))

test = PathFinding(rootNode=(214,218),path=path)
test.GUI()
