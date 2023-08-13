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
        self.showVisualization=False

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

    def printTree(self):
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
    def updateVisualization(self, node):
        pass

    def find(self, goal=None, searchtype='BFS', avoidRepeat='path', print_steps=False, stepByStep=False, showVisualization=False, iteractionsLimit=-1):
        """
        Main method, used to find the solution in the initialized search tree

        goal -> represents the objective of the search

        searchtype  -> BFS, Breadth-first search
                    -> DFS, Deep-first search
                    -> IDDFS, Iterative Deepening Deep-first search
                    -> Greedy BFS, Greedy Best-first search
                    -> A*
                    -> IDA*, Iterative Deepening A*

        avoidRepeat -> parent, check only if the parent is the same
                    -> path, searches in the path between the root node and the current node
                    -> Tree, searches in all the tree

        print_steps -> If true, it prints the tree, the fringe at every iteration

        stepByStep  -> If true, starts in a interactive mode, in which executes one iteration at the time waiting for the user input

        showVisualization -> If true, calls the method UpdateVisualization every 100 iterations

        iteractionsLimit -> Limit the iteraction number, set to -1 to disable
        """
        
        #save the starting time
        start_time = time.time() 
        
        #set up some local variables
        self.showVisualization=showVisualization
        if goal!= None: self.goal=goal

        #check if a goal was given
        if self.goal==None:
            print("No goal given")
            return None

        #initialize the root node
        if searchtype in ['A*', 'IDA*', 'GreedyBFS']:
            self.root.heuristic=self.getHeuristic(self.root)
        if searchtype in ['A*', 'IDA*']:
            self.root.actionCost=0
            self.root.totalCost=self.root.actionCost+self.root.heuristic
        if searchtype == 'IDA*':
            self.ALimit = self.root.totalCost

        #initialize the fringe
        self.fringe=[self.root]

        #count the iteration to show stats at the end of the search or to limit them
        iterations=0

        #for memory usage stats
        removed_nodes=0 
        max_nodes=0

        #Main loop
        while(1):
            #debug code
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

            #check if we are at a dead end
            if (len(self.fringe)<1):
                print("No path found")
                return None
            
            #choose the next node
            Node=self.chooseNextNode(searchtype, print_steps)
            
            #debug code
            if(print_steps):
                print("Choosen node: "+str(Node.data),end='')
                if searchtype=='A*':
                    print(str(round(Node.totalCost,2)))
                elif searchtype=='GreedyBFS':
                    print(str(round(Node.heuristic,2)))
                else:
                    print("")

            #if enabled, update the visualization
            if(showVisualization):
                if iterations%100==0: #update visualization every 100 iterations
                    self.updateVisualization(Node)

            #check if the node corresponds with our goal
            if(Node.data==self.goal): #success!
                #os.system('cls' if os.name == 'nt' else 'clear') #clear terminal
                if(print_steps):
                    self.printTree()
                returnDict={}
                returnDict["path"]=self.pathTo(Node)
                returnDict["iterations"]=iterations
                returnDict["time"]=round(time.time() - start_time,2)
                returnDict["expNodes"]=self.ID
                returnDict["maxNodes"]=max_nodes
                returnDict["Depth"]=Node.get_depth()
                
                return returnDict
            
            #expand the node
            childs=self.expandNode(Node) #get the childs list
            
            #check if there are repeats in the same branch (if selected)
            self.deleteRepeats(childs, Node, avoidRepeat) 
            
            #if the node has childs, add them to the tree and the fringe
            #if the node doesn't have childs, it can be removed from the tree
            if(len(childs)>0):
                self.addChildsToTree(childs)
                self.appendToFringe(childs, searchtype) #append to fringe
            else:
               #the node doesn't have childs, so it can be removed from the tree
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
            
            #iteractions counter
            iterations+=1

            #track the number of nodes to have some statistics
            if (self.ID-removed_nodes)>max_nodes:
                max_nodes=self.ID-removed_nodes

            #check if the iteraction limit was reach
            if(iteractionsLimit!=-1):
                if(iterations>iteractionsLimit):
                    #input("Reached interactions limit, press ENTER to exit...")
                    #print("Max iterations reached")
                    return None
            
            if(stepByStep):
                input("Press Enter to continue...")
                os.system('cls' if os.name == 'nt' else 'clear')

