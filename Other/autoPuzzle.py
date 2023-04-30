import sys
sys.path.append('../SearchTree')
from SearchTree import NPuzzleSearchTree
import pyautogui
import time

"""
This script implements the NPuzzle solver and the inputs the mouse clicks to automatically solve the puzzle

N is the size of the grid 15Puzzle -> N=4

xBase is the x coordinate of the center of the upper-left square
yBase is the same, but for the y coordinate
spac is the spacing between two squares
"""
N=4

deltaT=100 #ms

if N==3:
    xBase=350
    yBase=425
    spac=120
elif N==4:
    xBase=280
    yBase=425
    spac=125

#pyautogui.click(xBase+3*spac,yBase+0*spac)
#exit()

def solvable(tiles, N):
    #Source: https://www.geeksforgeeks.org/check-instance-15-puzzle-solvable/
    count = 0

    for i in range(N*N-1):
        for j in range(i+1, N*N):
            if tiles[j] and tiles[i] and tiles[i] > tiles[j]:
                count += 1
    print("Inversions number:" + str(count))

    if N==3:
        return count % 2 == 0
    elif N==4:
        row=0
        for i,val in enumerate(tiles):
             if val=='0':
                  row=int((i+1)/4)
                  break
        if row%2==0:
            print("Blank in even row")
            return count%2==0
        else:
             print("Blank in odd row")
             return count%2==1
    return False

inp = input("Insert tiles: ").split(" ")
while "" in inp:  # remove empty strings or double spaces
            inp.remove("")

if not solvable(inp,N):
     print("Not solvable!")
     #exit()
else:
     print("Should be solvable")

start=[]
for y in range(N):
    tmp=[]
    for x in range(N):
        tmp.append(int(inp[y*N+x]))
    start.append(tmp)

#for i in range(16):
#    if i not in inp:
#        print("Invalid input, not present: "+str(i))

print(start)
tree = NPuzzleSearchTree(start)

path = tree.find(searchtype='GreedyBFS', avoidRepeat="currentTree", stepByStep=False, print_steps=False, iteractionsLimit=-1)
input("press ENTER to autocomplete")
# for el in path:
#     print("->"+str(el))
a=0
for i, step in enumerate(path):
    for y, row in enumerate(step):
        for x, el in enumerate(row):
            if el == 0:
                pyautogui.click(xBase+x*spac,yBase+y*spac)
                a+=1
        else:
            continue
        break
print(a)
    #time.sleep(deltaT/1000)