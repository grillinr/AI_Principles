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

% Define the heuristic as the straight-line distance to Bucharest
dist(arad, 366).
dist(bucharest, 0).
dist(craiova, 160).
dist(drobeta, 242).
dist(eforie, 161).
dist(fagaras, 176).
dist(giurgiu, 77).
dist(hirsova, 151).
dist(iasi, 226).
dist(lugoj, 244).
dist(mehadia, 241).
dist(neamt, 234).
dist(oradea, 380).
dist(pitesti, 100).
dist(rimnicu_vilcea, 193).
dist(sibiu, 253).
dist(timisoara, 329).
dist(urziceni, 80).
dist(vaslui, 199).
dist(zerind, 374).

% Define a bidirectional road rule
connected(X, Y, D) :- road(X, Y, D).
connected(X, Y, D) :- road(Y, X, D).

% Greedy Search to reach Bucharest from any starting city
% While maintaing what has been visited
greedy(Start) :-
    greedy_helper([[Start]], []).

% Case where Bucharest is found
greedy_helper([[bucharest | Path] | _], _) :-
    reverse([bucharest | Path], FullPath),
    write('Path: '), write(FullPath), nl, !.

greedy_helper([[Current | Path] | Queue], Visited) :-
    % generate new paths
    findall([Next, Current | Path],
        (connected(Current, Next, _), \+ member(Next, [Current | Path])), NewPaths),
    
    % Sort new paths by straight-line distance to Bucharest
    sort_by_distance(NewPaths, SortedNewPaths),
    
    % Append sorted paths to the queue
    append(SortedNewPaths, Queue, UpdatedQueue),
    greedy_helper(UpdatedQueue, [Current | Visited]).

% Sort paths by distance
sort_by_distance(Paths, Sorted_Paths) :-
    % Map list of Paths to each ones distance
    map_list_to_pairs(heuristic_function, Paths, Dist_Path_Pairs),
    keysort(Dist_Path_Pairs, Sorted_Dist_Path_Pairs),
    pairs_values(Sorted_Dist_Path_Pairs, Sorted_Paths).
    
% Explicit Heuristic Function 
% Needed to map path list to their distance
heuristic_function([City | _], Dist) :-
    dist(City, Dist).
    
