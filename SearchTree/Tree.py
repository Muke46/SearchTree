from abc import ABC, abstractmethod
from SearchTree import Node
import os
import time
from operator import attrgetter

class Tree(ABC):
    def __init__(self, rootNode):
        self.root = Node(rootNode)
        self.root.heuristic=self.getHeuristic(self.root)
        self.root.actionCost=0
        self.root.totalCost=self.root.actionCost+self.root.heuristic
        self.fringe=None
        self.ID = 0
        self.root.ID = self.ID
        self.hashl=[]
        self.depthLimit = 0
        #self.scoreLimit
    def getRoot(self):
        return self.root
    def getFringe(self):
        return self.fringe
    def addNode(self, node):
        node.parent.add_child(node)
    def newNode(self, data, parent):
        n=Node(data)
        self.ID+=1
        n.ID=self.ID
        n.parent=parent
        n.hash=hash(str(data))
        return n
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
    @abstractmethod
    def getHeuristic(self, node):
        pass
    @abstractmethod
    def getActionCost(self, beginNode, endNode):
        pass
    
    def chooseNextNode(self, searchtype):
        match searchtype:
            case 'BFS':
                return self.fringe.pop(0)
            case 'DFS':
                return self.fringe.pop(0)
            case 'GreedyBFS':
                i=0
                while True:
                    if i in self.fringe:
                        if(len(self.fringe[i])>0):
                            return self.fringe[i].pop(0)
                    i+=1
                bestNode=self.fringe[0]
                for el in self.fringe:
                    if(el.heuristic<bestNode.heuristic):
                        bestNode=el
                self.fringe.remove(bestNode)
                return bestNode
            case 'A*':
                # bestScore = bestNode.heuristic+bestNode.actionCost
                # for el in self.fringe:
                #     score = el.heuristic + el.actionCost
                #     if(score<bestScore):
                #         bestNode=el
                #         bestScore=score
                
                #bestNode = min(self.fringe, key=attrgetter('totalCost'))
                #self.fringe.remove(bestNode)
                #return bestNode

                i=0
                while True:
                    if i in self.fringe:
                        if(len(self.fringe[i])>0):
                            return self.fringe[i].pop(0)
                    i+=1

                
            case 'IDA*':
                bestNode=self.fringe[0]
                bestScore = bestNode.heuristic+bestNode.actionCost
                for el in self.fringe:
                    score = el.heuristic + el.actionCost
                    if(score<bestScore):
                        bestNode=el
                        bestScore=score
                self.fringe.remove(bestNode)
                return bestNode
            case 'IDDFS':
                for el in self.fringe:
                    if el.get_depth()<self.depth:
                        self.fringe.remove(el)
                        return el
                #no node found at current depth
                print("No solution at depth: "+str(self.depth))
                self.depthLimit+=1
                
                return self.chooseNextNode(searchtype)
        #return node
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
                        pass #TODO #check if the node was ever added in the tree (even if it was deleted after) [need to keep the nodes or keep a list somewhere ->hash list?]
    
    def appendToFringe(self, childList, searchtype):
        match searchtype:
            case 'BFS':
                for el in childList:
                    self.fringe.append(el)
            case 'DFS':
               for el in childList:
                    self.fringe.insert(0, el)
            case 'GreedyBFS':
                for el in childList:
                    el.heuristic=self.getHeuristic(el)
                    if el.heuristic in self.fringe:
                        self.fringe[el.heuristic].append(el)
                    else:
                        self.fringe[el.heuristic]=[el]
                    #self.fringe.append(el)
            case 'A*':
                for el in childList:
                    el.heuristic=self.getHeuristic(el)
                    el.actionCost=self.getActionCost(el.parent, el)+el.parent.actionCost
                    el.totalCost=el.heuristic+el.actionCost
                    if el.totalCost in self.fringe:
                        self.fringe[el.totalCost].append(el)
                    else:
                        self.fringe[el.totalCost]=[el]
                    #self.fringe.append(el)
            case 'IDDFS':
               for el in childList:
                    self.fringe.insert(0, el)
    def addChildsToTree(self, childList):
        for el in childList:
            el.parent.add_child(el)
            self.hashl.append(el.hash)

    def find(self, goal=None, searchtype='BFS', avoidRepeat='path', print_steps='true', stepByStep='false', iteractionsLimit=-1):
        start_time = time.time()
        if(goal!=None):
            self.goal=goal

        if searchtype=='A*' or searchtype=='GreedyBFS':
            self.fringe=dict([(self.root.totalCost,[self.root])])
        else:
            self.fringe=[]
            self.fringe.append(self.root)

        iterations=0
        while(1):
            if(print_steps=='true'):
                print("Step: "+str(iterations))
                self.printTree()
                print("Fringe:")
                tmplst=[]

                # for el in self.fringe:
                #     print("|-"+str(el.data)+" \t[" + str(el.ID)+"]", end='')
                #     if (searchtype=='GreedyBFS'):
                #         print(" \theuristic{" + str(round(el.heuristic,2))+ "}")
                #     elif(searchtype=='A*'):
                #         print( " \ttheuristic{" + str(round(el.heuristic,2))+ "} \tpath cost{"+str(round(el.actionCost,2))+"} \tsum{"+str(round(el.heuristic+el.actionCost,2))+"}")
                #     else:
                #         print("")

            #check if we are at a dead end
            if (len(self.fringe)<1):
                print("No path found")
                return []
            
            #choose the next node
            Node=self.chooseNextNode(searchtype)
            print("Choosen node: "+str(Node.data),end=' ')
            print(str(round(Node.heuristicx,2)))
            if(print_steps=='true'):
                print("Choosen node: "+str(Node.data),end='')
                if searchtype=='A*':
                    print(str(round(Node.heuristic+Node.actionCost,2)))
                else:
                    print("")

            #check if the node corresponds with our goal
            if(Node.data==self.goal): #success!
                #os.system('cls' if os.name == 'nt' else 'clear')
                if(print_steps=='true'):
                    self.printTree()
                print("Solution:", end=" ")
                print(self.pathTo(Node))
                print("Solution found with "+ str(iterations)+" steps!")
                print("Elapsed time: "+str(round(time.time() - start_time,2))+" s")
                print("Expanded nodes: " + str(self.ID))
                print("Solution found at depth: " +str(Node.get_depth()))
                #input("Press Enter to exit...")
                return self.pathTo(Node)
            #expand the node
            childs=self.expandNode(Node) #get the childs list
            
            self.deleteRepeats(childs, Node, avoidRepeat) #check if there are repeats in the same branch (if selected)
            
            if(len(childs)>0):
                self.addChildsToTree(childs)
                self.appendToFringe(childs, searchtype)#append to fringe
            iterations+=1
            if(iteractionsLimit!=-1):
                if(iterations>iteractionsLimit):
                    input("Reached iteractions limit, press ENTER to exit...")
                    return None
            
            if(stepByStep=='true'):
                input("Press Enter to continue...")
                os.system('cls' if os.name == 'nt' else 'clear')

