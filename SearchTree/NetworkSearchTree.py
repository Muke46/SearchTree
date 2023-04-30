from SearchTree import Node, Tree
import math
class NetworkSearchTree(Tree):
    def __init__(self, rootNode, networkAdjList, citiesCoords=None):
        super().__init__(rootNode)
        self.network=networkAdjList
        if citiesCoords==None:
            print("Warning, cities coordinates not specified, A* and GreedyBFS will not work")
        self.coords=citiesCoords
        
        
    def getHeuristic(self, node):
        if self.coords != None and self.goal != None:
            return int(math.dist( list(self.coords[self.goal]), list(self.coords[node.data]) ))
        else:
            raise Exception("coords or goal not specified")

    def getActionCost(self, beginNode, endNode):
        lst=[item for item in self.network[beginNode.data] if item[0] == endNode.data]
        if(len(lst)>0):
            return(lst[0][1])
        else:
            return None
            
    def expandNode(self, node):
        childList=[]
        for child in self.network[node.data]:
            n = Node(child[0])
            n.parent=node

            childList.append(n)
        return childList
    
    def updateVisualization(self, node):
        pass