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

import time
from PIL import Image
import random
import os

q = queue.Queue()
imgpath=".\maze.png"

mouse_ctrl = False
maze_width = 499
maze_height = 799

def generate_maze(width, height):
    # Initialize the maze grid
    maze = [[1] * width for _ in range(height)]
    
    # Starting and ending points
    start_x, start_y = 1, 1
    end_x, end_y = width - 2, height - 2
    maze[start_y][start_x] = 0
    maze[end_y][end_x] = 0
    
    # Recursive backtracking to generate the maze
    stack = [(start_x, start_y)]
    while stack:
        x, y = stack[-1]
        neighbors = []
        for dx, dy in [(2, 0), (-2, 0), (0, 2), (0, -2)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 1:
                neighbors.append((nx, ny))
        if neighbors:
            nx, ny = random.choice(neighbors)
            maze[ny][nx] = 0
            maze[y + (ny - y) // 2][x + (nx - x) // 2] = 0
            stack.append((nx, ny))
        else:
            stack.pop()
    
    # Draw the maze as an image
    maze_img = Image.new("RGB", (width, height), "black")
    maze_pixels = maze_img.load()
    for y in range(height):
        for x in range(width):
            if maze[y][x] == 0:
                maze_pixels[x, y] = (255, 255, 255)

    # Save the maze as a JPEG image
    maze_img.save(imgpath)  

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
    test = PathFinding_GUI(rootNode=rootNode, path=imgpath)
    start_time=time.time()
    result=test.find(goal=goal, print_steps=False, stepByStep=False, showVisualization=True, avoidRepeat="Tree", searchtype="A*")
    if result==None:
        print('No solution found')
        return
    print(f'Solved in {time.time()-start_time:.2f}s e {result["iterations"]} iterazioni')
    
    path=result['path']
    print(f'Path lenght {len(path)}')

    for el in path:
        tmp=test.vismap.copy()
        tmp[test.root.data[0]][test.root.data[1]] = [0,0,255]
        tmp[test.goal[0]][test.goal[1]] = [0,255,0]
        for el in path:
            tmp[el[0]][el[1]] = [0, 255, 0]
        q.put(tmp)
    os._exit(1)


#generate_maze(maze_width, maze_height)

pygame.init()
data= mpimg.imread(imgpath)
print(data.shape)
scrnSize=(min(data.shape[0],1800),min(data.shape[1],700))
scrn = pygame.display.set_mode(scrnSize, pygame.RESIZABLE) #?



imp = pygame.surfarray.make_surface(data)
imp = pygame.transform.scale(imp, scrnSize)
scrn.blit(imp, (0, 0))



asd=0
#while q.empty():
#    pass
#img=q.get()
status = True

start=(1, 1)
goal=(data.shape[0]-4,data.shape[1]-2)

t = Thread(target=worker, args=(start,goal))
t.start()

while (status):
# iterate over the list of Event objects
    if not q.empty():
        img=q.get()
        asd+=1
        
        imp = pygame.surfarray.make_surface(img)
        imp = pygame.transform.scale(imp, scrnSize)
        if asd%1000==0: pygame.image.save(imp, f'C:\Files\SearchTree\Tests\Screens\Mazesolver{asd}.png')
        scrn.blit(imp, (0, 0))

    pygame.display.flip()

    if(mouse_ctrl):
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

    for event in pygame.event.get():               
        if event.type == pygame.VIDEORESIZE:
            scrnSize=pygame.display.get_surface().get_size()
            imp = pygame.transform.scale(imp, scrnSize)
            scrn.blit(imp, (0, 0))
        elif event.type == pygame.QUIT:
            status = False