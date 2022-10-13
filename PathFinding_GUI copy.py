import queue
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons, Button, TextBox

from SearchTree import Node, Tree
from PathFinding import PathFinding
from math import dist

import pygame
from threading import Thread
import matplotlib.image as mpimg

q = queue.Queue()

class PathFinding_GUI(PathFinding):
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

def worker():
    test = PathFinding_GUI(rootNode=(16,5), path="Resources\home_map.png")
    path=test.find(goal=(195,120), print_steps=False, stepByStep=False, showVisualization=True, avoidRepeat="Tree", searchtype="A*")
    for el in path:
        tmp=test.vismap.copy()
        tmp[test.root.data[0]][test.root.data[1]] = [0,0,255]
        tmp[test.goal[0]][test.goal[1]] = [0,255,0]
        for el in path:
            tmp[el[0]][el[1]] = [0, 255, 0]
        q.put(tmp)
        
pygame.init()
data= mpimg.imread("D:\Git\SearchTree\Resources\home_map.jpg")
scrn = pygame.display.set_mode((1280, 720)) #?

t = Thread(target=worker)
t.start()

while q.empty():
    pass
img=q.get()
status = True
while (status):
# iterate over the list of Event objects
    if not q.empty():
        img=q.get()
    imp = pygame.surfarray.make_surface(img)
    imp = pygame.transform.scale(imp, (1280, 720))
    scrn.blit(imp, (0, 0))

    pygame.display.flip()

    for i in pygame.event.get():

        if i.type == pygame.QUIT:
            status = False



#path = test.find(goal=(154,198), print_steps=False, stepByStep=False, showVisualization=False, avoidRepeat="Tree", searchtype="A*")
#print(path)
#test.GUI()