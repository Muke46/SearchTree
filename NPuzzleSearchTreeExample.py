from SearchTree import NPuzzleSearchTree

nx=4
ny=4
#
start = [[3,2,8],[6,4,7],[1,5,0]]
#start = [[1,2,0],[4,5,6],[7,3,8]]
start = [[7, 2, 1, 8], [9, 3, 4, 11],[5, 13, 6, 0],  [12, 10, 15, 14]]
print(start)
tree = NPuzzleSearchTree(start)

path = tree.find(searchtype='A*', avoidRepeat=None, stepByStep='false', print_steps='false', iteractionsLimit=-1)
#input("")
#for el in path:
#    print("->"+str(el))
