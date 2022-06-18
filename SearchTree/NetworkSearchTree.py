from SearchTree import Node, Tree

class NetworkSearchTree(Tree):
    def __init__(self, rootNode, networkAdjList, heuristic_fun):
        self.network=networkAdjList
        self.h_fun=heuristic_fun
        super().__init__(rootNode)
        
    def getHeuristic(self, node):
        return self.h_fun[node.data]
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
            #newNode = Node(child[0])
            #newNode.parent=node
            #self.ID+=1
            #newNode.ID=self.ID
            childList.append(n)
        return childList
