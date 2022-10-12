from abc import ABC, abstractmethod
from pickle import FALSE

from SearchTree import Node
import os
import time

class Tree(ABC):
    def __init__(self, rootNode):
        self.root = Node(rootNode)
        self.goal=None
        self.fringe=None
        self.ID = 0 #every node has an unique ID
        self.root.ID = self.ID #the root node have ID=0
        self.ID+=1
        self.hashl=[self.root.hash] #hash list of the current tree to speed up duplicate searches
        self.depthLimit = 0 #used for IDDF searches
        #self.scoreLimit

    def getRoot(self):
        return self.root

    def getFringe(self):
        return self.fringe

    def addNode(self, node):
        node.parent.add_child(node)

    def addChildsToTree(self, childList):
        for el in childList:
            el.parent.add_child(el)
            self.hashl.append(el.hash)
            el.ID=self.ID
            self.ID+=1


    def removeNode(self, node):
        node.kill_node()

    def getNodeDepth(self, node):
        depth=0
        p = node.parent
        while p:
            depth += 1
            p = p.parent
        return depth

    def printTree(self):  #TODO remove from the node class
        self.root.print_tree()

    def resetTree(self):
        self.root.childrens=[]
        self.fringe=[self.root]
        self.hashl=[]
        self.ID=0

    @abstractmethod
    def getHeuristic(self, node):
        pass
    @abstractmethod
    def getActionCost(self, beginNode, endNode):
        pass
    
    def chooseNextNode(self, searchtype, print_steps):
        match searchtype:
            case 'BFS':
                return self.fringe.pop(0)

            case 'DFS':
                return self.fringe.pop(0)

            case 'GreedyBFS':
                bestNode=self.fringe[0]
                for el in self.fringe:
                    if(el.heuristic<bestNode.heuristic):
                        bestNode=el
                self.fringe.remove(bestNode)
                return bestNode

            case 'A*':
                #initialize "bestNode" to the first node
                bestNode=self.fringe[0]
                #loop though the list to find a better node
                for el in self.fringe: 
                    if(el.totalCost<bestNode.totalCost):
                        bestNode=el
                #remove the node from the list and return it
                self.fringe.remove(bestNode)
                return bestNode

            case 'IDA*':
                #search for a node that have a totalCost below the current limit
                for el in self.fringe:
                    if el.totalCost<=self.ALimit:
                        self.fringe.remove(el)
                        return el
                #no node satisfies the condition
                if print_steps: print("Nothing found with cost:"+str(self.ALimit))
                
                #pick a new limit
                self.ALimit = self.fringe[0].totalCost
                for el in self.fringe:
                    if el.totalCost<self.ALimit:
                        self.ALimit=el.totalCost
            
                #delete current tree
                self.resetTree()
                return self.chooseNextNode(searchtype, print_steps)
                
            case 'IDDFS':
                for el in self.fringe:
                    if(el.get_depth()<=self.depthLimit):
                        self.fringe.remove(el)
                        return el
                if print_steps:
                    print("Nothing found at depth:"+str(self.depthLimit))
                #delete current tree
                self.resetTree()
                self.depthLimit+=1
                return self.chooseNextNode(searchtype, print_steps)

    def pathTo(self, node):
        path = []
        while node:
            path.insert(0,node.data) #append in front
            node=node.parent
        return path
        
    @abstractmethod
    def expandNode(self, node):
        #return child list
        pass
    def deleteRepeats(self,childList, node, avoidRepeat):
        if(avoidRepeat!='None'):
            for el in list(childList): #iterate over a copy of the list
                #print(el.data)
                match avoidRepeat:
                    case "parent":
                        if(el.data==el.parent):
                            childList.remove(el)
                            continue
                    case "path":
                        p = el.parent
                        while p:
                            if(p.data==el.data):
                                childList.remove(el)
                                break
                            p=p.parent
                        continue
                    case "currentTree": #check in the current search tree
                        if el.hash in self.hashl:
                            childList.remove(el)
                    case "Tree":
                        if el.hash in self.hashl:
                            childList.remove(el)
    
    def appendToFringe(self, childList, searchtype):
        match searchtype:
            case 'BFS':
                for el in childList:
                    self.fringe.append(el)
            case 'DFS' | 'IDDFS':
               for el in childList:
                    self.fringe.insert(0, el)
            case 'GreedyBFS':
                for el in childList:
                    el.heuristic=self.getHeuristic(el)
                    self.fringe.append(el)

            case 'A*' | 'IDA*':
                for el in childList:
                    el.heuristic=self.getHeuristic(el)
                    el.actionCost=self.getActionCost(el.parent, el)+el.parent.actionCost
                    el.totalCost=el.heuristic+el.actionCost
                    self.fringe.append(el)
    @abstractmethod
    def showVisualization(self, node):
        pass

    def find(self, goal=None, searchtype='BFS', avoidRepeat='path', print_steps=False, stepByStep=False, showVisualization=False, iteractionsLimit=-1):
        start_time = time.time() #save the starting time
        
        if goal!= None: self.goal=goal

        if self.goal==None:
            print("No goal given")
            return []

        if searchtype in ['A*', 'IDA*', 'GreedyBFS']:
            self.root.heuristic=self.getHeuristic(self.root)
        if searchtype in ['A*', 'IDA*']:
            self.root.actionCost=0
            self.root.totalCost=self.root.actionCost+self.root.heuristic
        if searchtype == 'IDA*':
            self.ALimit = self.root.totalCost

        self.fringe=[self.root]

        #count the iteration to show stats at the end of the search or to limit them
        iterations=0

        #for memory usage stats
        removed_nodes=0 
        max_nodes=0
        while(1):
            if(print_steps):
                print("Step: "+str(iterations))
                if searchtype=='IDDFS':
                    print("Depth Limit: "+str(self.depthLimit))
                if searchtype=='IDA*':
                    print("Cost Limit: "+str(self.ALimit))
                self.printTree()
                print("Fringe:")
                for el in self.fringe:
                    print("|-"+str(el.data)+" \t[ID:" + str(el.ID)+"] ", end='')
                    if searchtype=="BFS" or searchtype=="DFS" or searchtype=="IDDFS":
                         print("(depth: "+str(el.get_depth())+")")
                    elif searchtype=="A*" or searchtype=="IDA*":
                        print("Action Cost:"+str(el.actionCost)+" Heuristic:"+str(el.heuristic)+" Total:"+str(el.totalCost))

            if(showVisualization):
                if iterations%300==0:
                    self.showVisualization()

            #check if we are at a dead end
            if (len(self.fringe)<1):
                print("No path found")
                return []
            
            #choose the next node
            Node=self.chooseNextNode(searchtype, print_steps)

            if(print_steps):
                print("Choosen node: "+str(Node.data),end='')
                if searchtype=='A*':
                    print(str(round(Node.totalCost,2)))
                elif searchtype=='GreedyBFS':
                    print(str(round(Node.heuristic,2)))
                else:
                    print("")

            #check if the node corresponds with our goal
            if(Node.data==self.goal): #success!
                os.system('cls' if os.name == 'nt' else 'clear') #clear terminal
                if(print_steps):
                    self.printTree()
                print("Solution:", end=" ")
                print(self.pathTo(Node))
                print("Solution found with "+ str(iterations)+" steps!")
                print("Elapsed time: "+str(round(time.time() - start_time,2))+" s")
                print("Expanded nodes: " + str(self.ID))
                print("Max nodes in memory: "+str(max_nodes))
                print("Solution found at depth: " +str(Node.get_depth()))
                return self.pathTo(Node)
            
            #expand the node
            childs=self.expandNode(Node) #get the childs list
            
            #check if there are repeats in the same branch (if selected)
            self.deleteRepeats(childs, Node, avoidRepeat) 
            
            if(len(childs)>0):
                #if searchtype=='A*':
                #    for ch in childs:
                #        ch.
                self.addChildsToTree(childs)
                self.appendToFringe(childs, searchtype) #append to fringe
            else:
               #if a node have no childs it can be removed from the tree
                n=Node
                while n.parent != None: #prune the dead branch, if any
                    n.kill_node()
                    removed_nodes+=1
                    if avoidRepeat != "Tree":
                        self.hashl.remove(n.hash)
                    if len(n.parent.childrens)==0: #if the parent have no childs we can delete it
                        n=n.parent
                    else:
                        break
            iterations+=1
            if (self.ID-removed_nodes)>max_nodes:
                max_nodes=self.ID-removed_nodes

            if(iteractionsLimit!=-1):
                if(iterations>iteractionsLimit):
                    input("Reached interactions limit, press ENTER to exit...")
                    return []
            
            if(stepByStep):
                input("Press Enter to continue...")
                os.system('cls' if os.name == 'nt' else 'clear')

