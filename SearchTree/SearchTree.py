from Node import Node
from Tree import Tree

class SearchTree:
    def __init__(self, rootNode, adjlist, heuristic_fun):
        self.tree=Tree(rootNode)
        #self.root = Node(rootNode)
        self.network=adjlist #ToToToDo find better name
        self.h_fun=heuristic_fun
        #self.tree.fringe=[]
        #self.tree.fringe.append(self.root)

    def norm_euristic(self):
        max = 0
        for el in self.h_fun:

            if(self.h_fun[el]>max):
                max=self.h_fun[el]
        for el in self.h_fun:
            self.h_fun[el]=self.h_fun[el]/max
    
    def norm_cost(self):
        max = 0
        for el in self.network:
            for cost in self.network[el]:
                if(cost[1]>max):
                    max=cost[1]        
        for el in self.network:
            for i in range(len(self.network[el])):
                self.network[el][i]=(self.network[el][i][0],round(self.network[el][i][1]/max,4)) #brutto brutto
        '''
        for cost in self.network[el]: #non funziona! why? idfk
                print(cost)
                cost=(cost[0],cost[1]/max)
                print(cost)
        '''
    
    def action_cost(self, beginNode, endNode):
        lst=[item for item in self.network[beginNode] if item[0] == endNode]
        if(len(lst)>0):
            return(lst[0][1])
        else:
            return None

    def find(self, goal, searchtype='BFS', avoidRepeat='path', print_steps='true', normalize_heuristic='false', normalize_cost='false'):
        print("Searching with "+searchtype+"...")
        
        #normalize heuristic
        if(normalize_heuristic=='true'):
            self.norm_euristic()

        #normalize cost
        if(normalize_cost=='true'):
            self.norm_cost()

        for i in range(10): #while(1): for per evitare loop infiniti
            #if the fringe is empty -> failure
            if len(self.tree.fringe)<1:
                print("No path found!")
                return [] #brutto?
            
            if(print_steps):
                print("Fringe [heuristic]: ",end="")
                for el in self.tree.fringe:
                    print(str(el.data)+" ["+f'{self.h_fun[el.data]:.2f}'+"]", end=", ")
                print("}")
            

            #choose a leaf node, and remove it from the fringe
            if (searchtype=='BFS' or searchtype=='DFS'):
                next_node = self.tree.fringe.pop(0)
            elif (searchtype=='GreedyBF'):
                best=self.tree.fringe[0]
                for el in self.tree.fringe:
                    if (self.h_fun[el.data]<self.h_fun[best.data]):
                        best=el
                next_node = best
                self.tree.fringe.remove(best)
            elif (searchtype=="A*"):
                best=self.tree.fringe[0]
                bestValue=2
                if(print_steps):
                    print("Fringe [heur+cost]: ", end="")
                for el in self.tree.fringe:
                    sum=self.h_fun[el.data] #add the heuristic function value
                    if(el.parent!=None):
                        sum+=self.action_cost(el.data,el.parent.data)
                    if(print_steps=='true'):
                        print(str(el.data)+" ["+str(round(sum,2))+"]",end=", ")
                    if (sum<bestValue):
                        #print("Best: "+str(bestValue)+" sum:"+str(sum))
                        bestValue=sum
                        best=el    
                if(print_steps):
                    print("}")
                next_node = best
                self.tree.fringe.remove(best)
            print("Expand: "+str(next_node.data))

            #if the choosen node is the goal -> success!
            if next_node.data==goal:
                print("(che)Success!")
                #genera il path
                path = []
                p = next_node
                while p:
                    path.append(p.data)
                    p = p.parent
                path.reverse()
                #root.print_tree()
                print("iterations: " + str(i))
                return path

            #expand the node, add the new nodes to the frontier
            for child in self.network[next_node.data]:
                #ToToToToDO check if the node is already in the tree
                newNode = Node(child[0])
                ok = 1
                
                match avoidRepeat:
                    case "none":
                        ok=1
                    case "parent": #check only parent
                        if(next_node.data==child[0]):
                            ok=0
                    case "path": #check in the same branch
                        p = next_node.parent
                        while p:
                            if(p.data==child[0]):
                                ok=0
                            p = p.parent
                    case "currentTree": #check in the current search tree
                        print("Not implemented")
                        return []
                    case "Tree": #check if the node was ever added in the tree (even if it was deleted after) [need to keep the nodes or keep a list somewhere]
                        print("Not implemented")
                        return []

                if ok:
                    if(searchtype=='BFS' or searchtype=='GreedyBF' or searchtype=='A*'): #per GBF e A* è in realtà indifferente l'ordine
                        self.tree.fringe.append(newNode)
                    elif(searchtype=='DFS'):
                        self.tree.fringe.insert(0,newNode)
                    next_node.add_child(newNode)
                    
        return []
    
    def showGui(self):
        self.gui.uiah()
        self.gui.test()