from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import matplotlib.image as mpimg
import time

from threading import Thread, Event

from SearchTree import Node, Tree
import math

data = mpimg.imread("D:\Git\SearchTree\Resources\home_map_exp5.png")

def GUI():
    test = PathFinding(rootNode=(214,218),data=data)
    input("Press ENTER to start")
    path = test.find(goal=(166,212), print_steps=False, stepByStep=False, showVisualization=True, avoidRepeat="Tree", searchtype="DFS")
    for el in path:
        data[el[0]][el[1]] = [0., 1., 0., 1.]

class PathFinding(Tree):
    def __init__(self, rootNode, data):
        super().__init__(rootNode)
        self.map = data.copy()
        self.vismap = data
        self.wallColor = [0., 0., 0., 1.]
        self.walkableColor = [1., 1., 1., 1.]

    def showVisualization(self):
        self.vismap[self.root.data[0]][self.root.data[1]] = [0., 0., 1., 1.]
        self.vismap[self.goal[0]][self.goal[1]] = [0., 1., 0., 1.]
        time.sleep(1/1000000)

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

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        pg.setConfigOptions(imageAxisOrder='row-major')
        self.imv = pg.ImageView()
        self.setCentralWidget(self.imv)
        self.resize(800,800)
        self.imv.ui.histogram.hide()
        self.imv.ui.roiBtn.hide()
        self.imv.ui.menuBtn.hide()
        self.imv.setImage(data)

        self.timer = QtCore.QTimer()

        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def mousePressEvent (self, eventQMouseEvent):
        print(self.imv.mapFromParent( eventQMouseEvent.pos()) )

    def update_plot_data(self):
        self.imv.setImage(data)

    def mouse_clicked(self, mouseClickEvent):
        # mouseClickEvent is a pyqtgraph.GraphicsScene.mouseEvents.MouseClickEvent
        print('clicked plot 0x{:x}, event: {}'.format(id(self), mouseClickEvent))

showGUI=True
if showGUI:
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
t = Thread(target=GUI)
t.start()

if showGUI:
    sys.exit(app.exec_())
