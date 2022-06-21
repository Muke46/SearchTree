from SearchTree import NetworkSearchTree

map = {
    "Arad" :          [("Zerind",75),("Timisoara",118),("Sibiu",140)],
    "Zerind" :        [("Arad",75),("Oradea",71)],
    "Timisoara" :     [("Arad",118),("Lugoj",111)],
    "Oradea" :        [("Zerind",71),("Sibiu",151)],
    "Sibiu"  :        [("Arad",140),("Oradea",151),("Rimnicu Vilcea",80),("Fagaras",99)],
    "Lugoj"  :        [("Timisoara",111),("Mehadia",70)],
    "Mehadia":        [("Lugoj",70),("Drobeta",75)],
    "Drobeta":        [("Mehadia",75),("Craiova",120)],
    "Craiova":        [("Drobeta",120),("Rimnicu Vilcea",146),("Pitesti",138)],
    "Rimnicu Vilcea": [("Sibiu",80),("Craiova",146),("Pitesti",97)],
    "Fagaras":        [("Sibiu",99),("Bucharest",211)],
    "Pitesti":        [("Rimnicu Vilcea",97),("Craiova",138),("Bucharest",101)],
    "Bucharest":      [("Fagaras",211),("Giurgiu",90),("Pitesti",101),("Urziceni",85)],
    "Giurgiu":        [("Bucharest",90)],
    "Urziceni":       [("Bucharest",85),("Hirsova",98),("Vaslui",142)],
    "Hirsova":        [("Urziceni",98),("Eforie",86)],
    "Eforie":         [("Hirsova",86)],
    "Vaslui":         [("Urziceni",142),("Iasi",92)],
    "Iasi":           [("Vaslui",92),("Neamt",87)],
    "Neamt":          [("Iasi",87)]
    }   
citiesCoords = {
    "Arad" :          (107,254),
    "Zerind" :        (154,146),
    "Timisoara" :     (115,477),
    "Oradea" :        (216,40),
    "Sibiu"  :        (423,346),
    "Lugoj"  :        (307,561),
    "Mehadia":        (315,668),
    "Drobeta":        (308,777),
    "Craiova":        (547,808),
    "Rimnicu Vilcea": (491,476),
    "Fagaras":        (692,368),
    "Pitesti":        (731,592),
    "Bucharest":      (947,700),
    "Giurgiu":        (875,854),
    "Urziceni":       (1100,638),
    "Hirsova":        (1308,640),
    "Eforie":         (1386,792),
    "Vaslui":         (1242,383),
    "Iasi":           (1144,213),
    "Neamt":          (961,132)
    }


start = "Arad"
goal  = "Bucharest"

#Calculate the heuristic function from the coordinates
heuristicFun = {}
for key in citiesCoords:
    heuristicFun[key] = (abs(citiesCoords[key][0]-citiesCoords[goal][0])+abs(citiesCoords[key][1]-citiesCoords[goal][1]))*0.26803 #scaling factor to make the calculated heuristic closer to the real distances


tree = NetworkSearchTree(start, map, heuristicFun)


path = tree.find(goal, searchtype='A*', avoidRepeat="path", stepByStep='false', print_steps='false')
print(path)
