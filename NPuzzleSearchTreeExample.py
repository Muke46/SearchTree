from SearchTree import NPuzzleSearchTree

nx=4
ny=4
#
start = [[3,2,8],[6,4,7],[1,5,0]]
#start = [[1,2,0],[4,5,6],[7,3,8]]
#start = [[5, 2, 12, 13], [8, 15, 4, 6],[11, 7, 3, 9],  [10, 14, 1, 0]]
print(start)
tree = NPuzzleSearchTree(start)

path = tree.find(searchtype='IDDFS', avoidRepeat="currentTree", stepByStep='false', print_steps='false', iteractionsLimit=-1)
input("")
for el in path:
    print("->"+str(el))
