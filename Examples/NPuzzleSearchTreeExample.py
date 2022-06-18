from SearchTree import NPuzzleSearchTree

nx=4
ny=4
#
start = [[1,3,0],[5,2,6],[4,7,8]]
start = [[4,5,3],[1,7,2],[6,8,0]]
start = [[1, 3, 6], [8, 7, 5], [4, 2, 0]]
start  = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,0,15]]
#start  = [[1,2,3,4],[6,8,5,9],[11,10,7,0]]
#start = [[5, 2, 12, 13], [8, 15, 4, 6],[11, 7, 3, 9],  [10, 14, 1, 0]]
#start = [[0,1],[2,3]]
print(start)
tree = NPuzzleSearchTree(start)

path = tree.find(searchtype='GreedyBFS', avoidRepeat="path", stepByStep='false', print_steps='true', iteractionsLimit=-1)
input("")
print(path)
