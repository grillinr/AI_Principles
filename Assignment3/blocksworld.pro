% init the world, and its blocks
blocks([a, b, c, d]).
block(X) :-
    blocks(BLOCKS),
    member(X, BLOCKS).

% simple not-equal check from instructions
notequal(X, Y) :- X \= Y.

% helper func that replaces all elements in a list
% the cut (!) prevents unnecessary backtracking
substitute(X, Y, [X|T], [Y|T]) :- !.
substitute(X, Y, [H|T], [H|T1]) :-
    substitute(X, Y, T, T1).

% check if a state hasn't been visited before
% uses negation of a state being a permutation of any visited state
notYetVisited(State, PathSoFar) :-
    \+ (member(OtherState, PathSoFar), 
        is_permutation(State, OtherState)).

% custom permutation check for better efficiency
% was getting stack overflow errors otherwise
is_permutation([], []).
is_permutation([H|T], L) :-
    select(H, L, L1),
    is_permutation(T, L1).


% SUPER IMPORTANT MOVING CASES
% here are a bunch of ways we can move 
% blocks, and how we do that
% move block X from block Y onto block Z
move(X, Y, Z, S1, S2) :-
    member([clear, X], S1),
    member([on, X, Y], S1),
    Y \= Z,
    member([clear, Z], S1),
    X \= Z,
    delete(S1, [on, X, Y], S1a),
    delete(S1a, [clear, Z], S1b),
    S2 = [[on, X, Z], [clear, Y] | S1b].

% move block X from block Y onto the table
move(X, Y, "table", S1, S2) :-
    member([clear, X], S1),
    member([on, X, Y], S1),
    Y \= "table",
    delete(S1, [on, X, Y], S1a),
    S2 = [[on, X, "table"], [clear, Y] | S1a].

% move block X from the table onto block Z
move(X, "table", Z, S1, S2) :-
    member([clear, X], S1),
    member([on, X, "table"], S1),
    member([clear, Z], S1),
    X \= Z,
    delete(S1, [on, X, "table"], S1a),
    delete(S1a, [clear, Z], S1b),
    S2 = [[on, X, Z] | S1b].

% path finding between states
% prints move details for debugging
path(S1, S2) :-
    (move(X, Y, Z, S1, S2), 
    write('move '), write(X), % found this syntax in other
    write(' from '), write(Y), % prolog code on the examples
    write(' to '), write(Z), nl).

% create one-way connection between states
connect(S1, S2) :- path(S1, S2).

% depth-limited search for goal state
depthFirst(X, [X], _, _) :- 
    goal(X),
    write('goal reached!'), nl.

% fail if we go too deep to prevent infinite recursion
% again, this was a problem with stack overflowing
depthFirst(_, _, _, Depth) :- 
    Depth > 20,
    !,
    fail.

% standard depth-first exploration
depthFirst(X, [X|Ypath], VISITED, Depth) :-
    Depth1 is Depth + 1, % weird syntax but it works?
    connect(X, Y),
    notYetVisited(Y, VISITED),
    depthFirst(Y, Ypath, [Y|VISITED], Depth1).

% start and goal states for the blocks world
% this is only one of the test cases we were given
% the writeup contains all three, and anything can
% be tested here
start([[on, a, b], [on, b, "table"], [on, c, d], [clear, c], [clear, a], [on, d, "table"]]).
goal([[on, d, a], [on, a, c], [on, c, b], [on, b, "table"], [clear, d]]).

% find solution path with depth limit
solve(Path) :-
    start(Start),
    depthFirst(Start, Path, [Start], 0).

% display full solution path
print_solution(Path) :-
    write('solution path:'), nl,
    print_states(Path).

% helper function for debugging
% recursively print all states in the path
print_states([]).
print_states([H|T]) :-
    write('state: '), write(H), nl,
    print_states(T).
