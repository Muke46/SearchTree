from SearchTree import NPuzzleSearchTree
import pyautogui
import time

xBase=300
yBase=370
spac=115

deltaT=1 #ms

inp = input("Insert tiles: ").split(" ")
while "" in inp:  # remove empty strings or double spaces
            inp.remove("")

start=[]
for y in range(4):
    tmp=[]
    for x in range(4):
        tmp.append(int(inp[y*4+x]))
    start.append(tmp)

for i in range(16):
    if i not in inp:
        print("Invalid input, not present: "+str(i))

print(start)
tree = NPuzzleSearchTree(start)

path = tree.find(searchtype='GreedyBFS', avoidRepeat="currentTree", stepByStep='false', print_steps='false', iteractionsLimit=-1)
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