from SearchTree import Node, Tree
import copy
import ujson

class NPuzzleSearchTree (Tree):
    def __init__(self, rootNode):
        
        self.h_fun = None
        self.xDim = len(rootNode[0])
        self.yDim = len(rootNode)
        self.goal = self.generateGoal()
        print(self.goal)
        super().__init__(rootNode)
        
    def generateGoal(self):
        goal = []
        n=1
        for i in range(self.yDim):
            row = []
            for j in range(self.xDim):
                row.append(n)
                n+=1
            goal.append(row)
        goal[self.yDim-1][self.xDim-1]=0
        return goal
    
    def getHeuristic(self, node):
        # sum=0
        # for i in range(1,self.xDim*self.yDim):
        #     statey, statex = self.findN(i, node.data)
        #     goaly, goalx = self.findN(i, self.goal)
        #     sum+=abs(statey-goaly)+abs(statex-goalx)
        # return sum
        sum = 0
        for y,row in enumerate(node.data):
            for x, val in enumerate(row):
                if val==0:
                    goalx=self.xDim-1
                    goaly=self.yDim-1
                else:
                    goaly=int((val-1)/self.yDim)
                    goalx=int((val-1)%self.xDim)
                sum+=abs(x-goalx)+abs(y-goaly)
        return sum
    def getActionCost(self, beginNode, endNode):
        return 1
    def findN(self,n,  nodedata):
        for i, e in enumerate(nodedata):
            try:
                return i, e.index(n)
            except ValueError:
                pass
        raise ValueError("{!r} is not in list".format(0)) #??
    
    def expandNode(self, node):
        childList=[]
        y, x = self.findN(0,node.data) #search for the empty position
        #check left
        if(x>0):
            tmp=ujson.loads(ujson.dumps(node.data))
            #tmp=copy.deepcopy(node.data)
            tmp[y][x]=tmp[y][x-1]
            tmp[y][x-1]=0
            newNode = self.newNode(tmp, node)
            newNode.parent=node
            childList.append(newNode)
        #check up
        if(y>0):
            tmp=ujson.loads(ujson.dumps(node.data))
            #tmp=copy.deepcopy(node.data)
            tmp[y][x]=tmp[y-1][x]
            tmp[y-1][x]=0
            newNode = self.newNode(tmp, node)
            newNode.parent=node
            childList.append(newNode)
        #check right
        if(x<self.xDim-1):
            tmp=ujson.loads(ujson.dumps(node.data))
            #tmp=copy.deepcopy(node.data)
            tmp[y][x]=tmp[y][x+1]
            tmp[y][x+1]=0
            newNode = self.newNode(tmp, node)
            newNode.parent=node
            childList.append(newNode)
        #check down
        if(y<self.yDim-1):
            tmp=ujson.loads(ujson.dumps(node.data))
            #tmp=copy.deepcopy(node.data)
            tmp[y][x]=tmp[y+1][x]
            tmp[y+1][x]=0
            newNode = self.newNode(tmp, node)
            newNode.parent=node
            childList.append(newNode)
        return childList
