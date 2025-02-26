% define roads and distances between cities
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

% define the heuristic as the straight-line distance to Bucharest
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


% define a bidirectional road rule
connected(X, Y, D) :- road(X, Y, D).
connected(X, Y, D) :- road(Y, X, D).



%************** BFS ****************%
% BFS to reach Bucharest from any starting city
bfs(Start) :-
    bfs_helper([[Start]], bucharest).

% case where bucharest is found
bfs_helper([[bucharest | Path] | _], _) :-
    % reverse the path as the path as been prepended,
    % not appended!
    reverse([bucharest | Path], FullPath),
    % using the ! (cut) operator stops the query
    % and only displays the first path found.
    % Note: without this, there will be many
    % more results
    write('Path: '), write(FullPath), nl, !.

bfs_helper([[Current | Path] | Queue], Dest) :-
    % generate new paths
    % finds every node Next connected to Current
    % ensures Next is not already in the current path
    % creates a partial path for each valid Next
    % and collects them into NewPaths
    findall([Next, Current | Path],
        (connected(Current, Next, _), \+ member(Next, [Current | Path])),
        NewPaths),
    % queue newly generated paths
    append(Queue, NewPaths, UpdatedQueue),
    bfs_helper(UpdatedQueue, Dest).

%************** END BFS ****************%



%************** DFS ****************%
% DFS to reach Bucharest from any starting city
dfs(Start) :-
    dfs_helper([Start], bucharest).

% case where Bucharest is found
dfs_helper([bucharest | Path], _) :-
    reverse([bucharest | Path], FullPath),
    write('Path: '), write(FullPath), nl, !.

dfs_helper([Current | Path], Dest) :-
    connected(Current, Next, _),
    \+ member(Next, [Current | Path]),
    dfs_helper([Next, Current | Path], Dest).

%************** END DFS ****************%



%************** GREEDY ****************%
% greedy search to reach Bucharest from any starting city
% while maintaing what has been visited
greedy(Start) :-
    greedy_helper([[Start]], []).

% case where Bucharest is found
greedy_helper([[bucharest | Path] | _], _) :-
    reverse([bucharest | Path], FullPath),
    write('Path: '), write(FullPath), nl, !.

greedy_helper([[Current | Path] | Queue], Visited) :-
    % generate new paths
    findall([Next, Current | Path],
        (connected(Current, Next, _), \+ member(Next, [Current | Path])), NewPaths),
    
    % sort new paths by straight-line distance to Bucharest
    sort_by_distance(NewPaths, SortedNewPaths),
    
    % append sorted paths to the queue
    % shortest distance gets added first
    % so the next city visited will be the 
    % city with shortest distance to Bucharest
    append(SortedNewPaths, Queue, UpdatedQueue),
    
    % Recursively perform greedy searches
    % using the updated priority queue
    greedy_helper(UpdatedQueue, [Current | Visited]).

% sort paths by distance
sort_by_distance(Paths, Sorted_Paths) :-
    % map list of Paths to each ones distance as the key
    map_list_to_pairs(heuristic_function, Paths, Dist_Path_Pairs),

    % sort pairs based on the key/distance to Bucharest
    keysort(Dist_Path_Pairs, Sorted_Dist_Path_Pairs),

    % remove the key values to get 
    % the cities in order
    pairs_values(Sorted_Dist_Path_Pairs, Sorted_Paths).
    
% explicit Heuristic Function 
% needed to map path list to their distance
heuristic_function([City | _], Dist) :-
    dist(City, Dist).

%************** END GREEDY ****************%
