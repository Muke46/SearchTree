from SearchTree import NPuzzleSearchTree

nx=4
ny=4
#
start = [[3,2,8],[6,4,7],[1,5,0]]
start = [[6,3,2],[1,7,8],[4,5,0]]
start = [[5, 1, 3, 0], [10, 7, 2, 4],[9, 6, 8, 12],  [13, 11, 15, 14]]
#start = [[4, 1, 13, 8], [7, 5, 3, 15],[10, 6, 14, 9],  [0, 2, 12, 11]]
print(start)
tree = NPuzzleSearchTree(start)

path = tree.find(searchtype='A*', avoidRepeat='Tree', stepByStep='false', print_steps='false', iteractionsLimit=-1)
input("")
for el in path:
    print("->"+str(el))
