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
            #return int(math.dist( list(self.coords[self.goal]), list(self.coords[node.data]) ))
            x1, y1 = self.coords[node.data]
            x2, y2 = self.coords[self.goal]
            return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        else:
            raise Exception("coords or goal not specified")


    def getActionCost(self, beginNode, endNode):
        if self.coords!=None:
            x1, y1 = self.coords[beginNode.data]
            x2, y2 = self.coords[endNode.data]
            return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        else:
            raise Exception("citiesCoords not specified")
        
        #lst=[item for item in self.network[beginNode.data] if item[0] == endNode.data]
        #if(len(lst)>0):
        #    return(lst[0][1])
        #else:
        #    return None
            
    def expandNode(self, node):
        childList=[]
        for child in self.network[node.data]:
            n = Node(child)
            n.parent=node

            childList.append(n)
        return childList
    
    def updateVisualization(self, node):
        pass