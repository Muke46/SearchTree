import sys
sys.path.append('../SearchTree')
import queue
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons, Button, TextBox

from SearchTree import Node, Tree
from SearchTree.PathFindingSearchTree import PathFindingSearchTree
from math import dist

import pygame
from threading import Thread
import matplotlib.image as mpimg

q = queue.Queue()
imgpath=".\Resources\citymap.jpg"

class PathFinding_GUI(PathFindingSearchTree):
    def __init__(self, rootNode=(0,0), path='', walkableColor = [255,255,255], heuristic = 'LineOfSight'):
        super().__init__(rootNode, path, walkableColor, heuristic)

    def updateVisualization(self, expandedNode):
        tmp=self.vismap.copy()
        tmp[self.root.data[0]][self.root.data[1]] = [0,0,255]
        tmp[self.goal[0]][self.goal[1]] = [0,255,0]

        n=expandedNode
        while n.parent != None:
            tmp[n.data[0]][n.data[1]] = [150,150,150]
            n=n.parent
        q.put(tmp)

def worker(rootNode, goal):
    test = PathFinding_GUI(rootNode=rootNode, path="Resources\maze2.png")
    path=test.find(goal=goal, print_steps=False, stepByStep=False, showVisualization=True, avoidRepeat="Tree", searchtype="DFS")
    for el in path:
        tmp=test.vismap.copy()
        tmp[test.root.data[0]][test.root.data[1]] = [0,0,255]
        tmp[test.goal[0]][test.goal[1]] = [0,255,0]
        for el in path:
            tmp[el[0]][el[1]] = [0, 255, 0]
        q.put(tmp)


pygame.init()
data= mpimg.imread(".\Resources\maze2.jpg")
print(data.shape)
scrnSize=(min(data.shape[0],1800),min(data.shape[1],700))
scrn = pygame.display.set_mode(scrnSize, pygame.RESIZABLE) #?



imp = pygame.surfarray.make_surface(data)
imp = pygame.transform.scale(imp, scrnSize)
scrn.blit(imp, (0, 0))




#while q.empty():
#    pass
#img=q.get()
status = True

while (status):
# iterate over the list of Event objects
    if not q.empty():
        img=q.get()
        imp = pygame.surfarray.make_surface(img)
        imp = pygame.transform.scale(imp, scrnSize)
        scrn.blit(imp, (0, 0))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button==1:
                x = pygame.mouse.get_pos()[0]/scrnSize[0]*data.shape[0]
                y = pygame.mouse.get_pos()[1]/scrnSize[1]*data.shape[1]
                start=(int(x),int(y))
            elif event.button==2:
                x = pygame.mouse.get_pos()[0]/scrnSize[0]*data.shape[0]
                y = pygame.mouse.get_pos()[1]/scrnSize[1]*data.shape[1]
                goal=(int(x),int(y))
            elif event.button==3:
                t = Thread(target=worker, args=(start,goal))
                t.start()

        elif event.type == pygame.VIDEORESIZE:
            scrnSize=pygame.display.get_surface().get_size()
            imp = pygame.transform.scale(imp, scrnSize)
            scrn.blit(imp, (0, 0))
        elif event.type == pygame.QUIT:
            status = False