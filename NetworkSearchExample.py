from SearchTree import NetworkSearchTree

map = {
    "Arad" :          [("Zerind",75),("Timisoara",118),("Sibiu",140)],
    "Zerind" :        [("Arad",75),("Oradea",71)],
    "Timisoara" :     [("Arad",118),("Lugoj",111)],
    "Oradea" :        [("Zerind",71),("Sibiu",151)],
    "Sibiu"  :        [("Arad",140),("Oradea",151),("Rimnicu Vil.",80),("Fagaras",99)],
    "Lugoj"  :        [("Timisoara",111),("Mehadia",70)],
    "Mehadia":        [("Lugoj",70),("Drobeta",75)],
    "Drobeta":        [("Mehadia",75),("Craiova",120)],
    "Craiova":        [("Drobeta",120),("Rimnicu Vil.",146),("Pitesti",138)],
    "Rimnicu Vil.":   [("Sibiu",80),("Craiova",146),("Pitesti",97)],
    "Fagaras":        [("Sibiu",99),("Bucharest",211)],
    "Pitesti":        [("Rimnicu Vil.",97),("Craiova",138),("Bucharest",101)],
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
    "Arad":             (41,98),
    "Zerind":           (59,56),
    "Timisoara":        (44,184),
    "Oradea":           (83,15),
    "Sibiu":            (163,133),
    "Lugoj":            (118,216),
    "Mehadia":          (121,257),
    "Drobeta":          (118,300),
    "Craiova":          (211,311),
    "Rimnicu Vil.":   (189,183),
    "Fagaras":          (267,142),
    "Pitesti":          (282,228),
    "Bucharest":        (365,270),
    "Giurgiu":          (337,329),
    "Urziceni":         (424,246),
    "Hirsova":          (505,247),
    "Eforie":           (535,305),
    "Vaslui":           (479,147),
    "Iasi":             (441,82),
    "Neamt":            (371,50)
    }


start = "Arad"
goal  = "Neamt"

tree = NetworkSearchTree(start, map, citiesCoords)


path = tree.find(goal, searchtype='A*', avoidRepeat="path", stepByStep=True, print_steps=True)
print(path)
