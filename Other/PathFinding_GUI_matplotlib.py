import sys
sys.path.append('../SearchTree')
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons, Button, TextBox

from SearchTree import Node, Tree
from SearchTree.PathFindingSearchTree import PathFindingSearchTree
from math import dist



class PathFinding_GUI(PathFindingSearchTree):
    def __init__(self, rootNode=(0,0), path='', walkableColor = [1., 1., 1., 1.], heuristic = 'LineOfSight'):
        super().__init__(rootNode, path, walkableColor, heuristic)

        self.vismap = mpimg.imread(path)

        self.goal = None
        self.start = None
        self.searchType = 'BFS'

        self.fig,self.im_ax = plt.subplots(1,1)
        self.im = self.im_ax.imshow(self.vismap)

        self.fig.canvas.mpl_connect('button_press_event', self.GUIonclick)

        #promptTxt_ax = self.fig.add_axes([0.05, 0.9, 0.15, 0.15])
        self.promptTxt = plt.text(0, -10, 'Left click to set the starting point')

        searchType_ax = self.fig.add_axes([0.05, 0.7, 0.15, 0.15])
        searchType_radio = RadioButtons(searchType_ax, ('BFS', 'DFS', 'A*'))
        searchType_radio.on_clicked(self.changeSearchType)

        startBtn_ax = self.fig.add_axes([0.05, 0.3, 0.15, 0.15])
        self.startBtn = Button(startBtn_ax, "Start!", color="red")
        self.startBtn.on_clicked(self.GUI_startBtn)

        resetBtn_ax = self.fig.add_axes([0.05, 0.1, 0.15, 0.15])
        resetBtn = Button(resetBtn_ax, "Reset")
        resetBtn.on_clicked(self.GUI_reset)

        plt.show()
    
    def showVisualization(self, expandedNode):
        tmp=self.vismap.copy()
        tmp[self.root.data[0]][self.root.data[1]] = [0., 0., 0.5, 1.]
        tmp[self.goal[0]][self.goal[1]] = [0., 1., 0., 1.]

        n=expandedNode
        while n.parent != None:
            tmp[n.data[0]][n.data[1]] = [0., 0.75, 0.75, 1.]
            n=n.parent
        self.im.set_data(tmp)
        plt.draw()
        #self.fig.canvas.draw_idle()
        plt.pause(1)

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
        if self.heuristic == 'LineOfSight':return (dist(self.goal,node.data))
        if self.heuristic == 'Manhattan':  return abs(self.goal[0]-node.data[0])+abs(self.goal[1]-node.data[1])

    #GUI functions

    def GUIonclick(self, event):
        if event.inaxes != self.im_ax: return
        if event.button==1:
            self.start = (int(event.ydata),int(event.xdata))
            print(self.start)
            if self.goal == None: self.promptTxt.set_text("Right click to set the goal")
            else: 
                self.promptTxt.set_text("Choose the algorithm and press Start!")
                self.startBtn.color = "green"
                #self.GUI_update()
        if event.button==3:
            self.goal = (int(event.ydata),int(event.xdata))
            print(self.goal)
            if self.start != None: 
                self.promptTxt.set_text("Choose the algorithm and press Start!")
                self.startBtn.color = "green"
                #self.GUI_update()
        tmp=self.vismap.copy()
        if self.goal != None:
            tmp[self.goal[0]][self.goal[1]] = [0., 1., 0., 1.]
        if self.start != None:
            tmp[self.start[0]][self.start[1]] = [0., 0., 1., 1.]
        self.im.set_data(tmp)
        self.GUI_update()
    
    def changeSearchType(self, label):
        self.searchType = label

    def GUI_startBtn(self, event):
        if self.goal == None:
            print("Goal not set!")
            return
        if self.start != None:
            self.root.data = self.start
        else:
            print("Start not set!")
            return

        self.map = mpimg.imread(self.path)
        self.vismap = mpimg.imread(self.path)
        self.resetTree()

        path_found=self.find(goal=self.goal, print_steps=False, stepByStep=False, showVisualization=True, avoidRepeat="Tree", searchtype=self.searchType)
        for el in path_found:
            self.vismap[el[0]][el[1]] = [0., 1., 0., 1.]
        self.im.set_data(self.vismap)
        self.GUI_update()

    def GUI_reset(self, event):
        print("Reset!")
        self.start = None
        self.goal = None
        self.map = mpimg.imread(self.path)
        self.vismap = mpimg.imread(self.path)
        self.resetTree()
        tmp=self.vismap.copy()
        if self.goal != None:
            tmp[self.goal[0]][self.goal[1]] = [0., 1., 0., 1.]
        if self.start != None:
            tmp[self.start[0]][self.start[1]] = [0., 0., 1., 1.]
        self.im.set_data(tmp)
        self.startBtn.color = "red"
        self.GUI_update
    
    def GUI_update(self):
        self.fig.canvas.draw_idle()
        plt.pause(1)
        print("done")

test = PathFinding_GUI(rootNode=(50,50), path="Resources\home_map.png")

#path = test.find(goal=(154,198), print_steps=False, stepByStep=False, showVisualization=False, avoidRepeat="Tree", searchtype="A*")
#print(path)
test.GUI()