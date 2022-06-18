from abc import ABC, abstractmethod
from SearchTree import Node
import os
'''
import matplotlib.pyplot as plt
from netgraph import Graph
'''

class Tree(ABC):
    def __init__(self, rootNode):
        self.root = Node(rootNode)
        self.root.heuristic=self.getHeuristic(self.root)
        self.root.actionCost=0 #?
        self.fringe=[]
        self.fringe.append(self.root)
        self.ID = 0
        self.root.ID = self.ID
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
                bestNode=self.fringe[0]
                for el in self.fringe:
                    if(el.heuristic<bestNode.heuristic):
                        bestNode=el
                self.fringe.remove(bestNode)
                return bestNode
            case 'A*':
                bestNode=self.fringe[0]
                bestScore = bestNode.heuristic+bestNode.actionCost
                for el in self.fringe:
                    score = el.heuristic + el.actionCost
                    if(score<bestScore):
                        bestNode=el
                        bestScore=score
                self.fringe.remove(bestNode)
                return bestNode
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
        lst=[]
        if(avoidRepeat!='None'):
            for el in childList:
                #print(el.data)
                match avoidRepeat:
                    case "parent":
                        if(el.data==el.parent):
                            childList.remove(el)
                            continue
                    case "path":
                        p = el.parent
                        ok=0
                        while p:
                            if(p.data==el.data):
                                ok=1
                            p=p.parent
                        if(ok==0):
                            lst.append(el)
                        continue
                    case "currentTree": #check in the current search tree
                        f=[self.root]
                        ok=1
                        while(len(f)>0 and ok==1):
                            e=f.pop(0)
                            if(e.data==el.data):
                                childList.remove(el)
                                ok=0
                            for i in e.childrens:
                                f.append(i)
                        continue
                    case "Tree":
                        pass #TODO #check if the node was ever added in the tree (even if it was deleted after) [need to keep the nodes or keep a list somewhere]
        return lst
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
                    self.fringe.append(el)
            case 'A*':
                for el in childList:
                    el.heuristic=self.getHeuristic(el)
                    el.actionCost=self.getActionCost(el.parent, el)
                    self.fringe.append(el)
    def addChildsToTree(self, childList):
        for el in childList:
            el.parent.add_child(el)
    def find(self, goal=None, searchtype='BFS', avoidRepeat='path', print_steps='true', stepByStep='false', iteractionsLimit=-1):
        if(goal!=None):
            self.goal=goal
        iterations=0
        while(1):
            if(print_steps=='true'):
                print("Step: "+str(iterations))
                self.printTree()
                print("Fringe:")
                tmplst=[]
                for el in self.fringe:
                    print("|-"+el.data+" \t[" + str(el.ID)+"]", end='')
                    if (searchtype=='GreedyBFS'):
                        print(" \theuristic{" + str(round(el.heuristic,2))+ "}")
                    elif(searchtype=='A*'):
                        print( " \ttheuristic{" + str(round(el.heuristic,2))+ "} \tpath cost{"+str(round(el.actionCost,2))+"} \tsum{"+str(round(el.heuristic+el.actionCost,2))+"}")
                    else:
                        print("")

            #check if we are at a dead end
            if (len(self.fringe)<1):
                print("No path found")
                return []
            
            #choose the next node
            Node=self.chooseNextNode(searchtype)
            if(print_steps=='true'):
                print("Choosen node: "+str(Node.data))

            #check if the node corresponds with our goal
            if(Node.data==self.goal): #success!
                os.system('cls' if os.name == 'nt' else 'clear')
                if(print_steps=='true'):
                    self.printTree()
                print("Solution:", end=" ")
                print(self.pathTo(Node))
                input("Solution found with "+ str(iterations)+" steps! Press Enter to exit...")
                return self.pathTo(Node)
            #expand the node
            childs=self.expandNode(Node) #get the childs list
            
            childs=self.deleteRepeats(childs, Node, avoidRepeat) #check if there are repeats in the same branch (if selected)
            
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

