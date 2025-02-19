% Define roads and distances between cities
road(arad, timisoara, 118).
road(arad, zerind, 75).
road(arad, sibiu, 140).
road(bucharest, fagaras, 211).
road(bucharest, giurgiu, 90).
road(bucharest, pitesti, 101).
road(bucharest, urziceni, 85).
road(craiova, drobeta, 120).
road(craiova, pitesti, 138).
road(craiova, rimnicu_vilcea, 146).
road(drobeta, mehadia, 75).
road(drobeta, craiova, 120).
road(eforie, hirsova, 86).
road(fagaras, sibiu, 99).
road(giurgiu, bucharest, 90).
road(hirsova, urziceni, 98).
road(iasi, neamt, 87).
road(iasi, vaslui, 92).
road(lugoj, mehadia, 70).
road(lugoj, timisoara, 111).
road(mehadia, drobeta, 75).
road(mehadia, lugoj, 70).
road(neamt, iasi, 87).
road(oradea, sibiu, 151).
road(oradea, zerind, 71).
road(pitesti, bucharest, 101).
road(pitesti, craiova, 138).
road(pitesti, rimnicu_vilcea, 97).
road(rimnicu_vilcea, craiova, 146).
road(rimnicu_vilcea, pitesti, 97).
road(rimnicu_vilcea, sibiu, 80).
road(sibiu, arad, 140).
road(sibiu, fagaras, 99).
road(sibiu, oradea, 151).
road(sibiu, rimnicu_vilcea, 80).
road(timisoara, arad, 118).
road(timisoara, lugoj, 111).
road(urziceni, bucharest, 85).
road(urziceni, hirsova, 98).
road(urziceni, vaslui, 142).
road(vaslui, iasi, 92).
road(vaslui, urziceni, 142).
road(zerind, arad, 75).
road(zerind, oradea, 71).

% Define a bidirectional road rule
connected(X, Y, D) :- road(X, Y, D).
connected(X, Y, D) :- road(Y, X, D).
