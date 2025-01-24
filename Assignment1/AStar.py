# In A* the queue is maintained in nondecreasing order of the evaluation function
# f(n) = g(n) + h(n) of the children of the current city to the goal city.
# (Note that there is some backtracking taking place here, because the algorithm
# may need to discard a current node and backtrack to a previous step.)
