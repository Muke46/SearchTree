from SearchTree import Node, Tree
import math
class NetworkSearchTree(Tree):
    def __init__(self, rootNode, networkAdjList, citiesCoords=None):
        self.network=networkAdjList
        if citiesCoords==None:
            print("Warning, cities coordinates not specified, A* and GreedyBFS will not work")
        self.coords=citiesCoords
        super().__init__(rootNode)
        
    def getHeuristic(self, node):
        if self.coords != None:
            return math.dist( list(self.coords(self.root.data)), list(self.coords(node.data)) )
        else:
            return 0 #fallback in case coords was not specified

    def getActionCost(self, beginNode, endNode):
        lst=[item for item in self.network[beginNode.data] if item[0] == endNode.data]
        if(len(lst)>0):
            return(lst[0][1])
        else:
            return None
            
    def expandNode(self, node):
        childList=[]
        for child in self.network[node.data]:
            n = self.newNode(child[0], node)
            childList.append(n)
        return childList
