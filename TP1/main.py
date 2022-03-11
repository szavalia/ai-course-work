from models import *
from heuristics import *
from algorithm_chooser import execute_algorithm

initial_state = State([[1,8,3],[4,5,2],[0,7,6]], [1,0])
initial_state.heuristic = total_squares(initial_state)
#initial_state = State([[1,2,3],[4,5,6],[0,7,8]], [2,0], 0)
root = Node(initial_state,None,0)
objective_state = State([[1,2,3],[4,5,6],[7,8,0]], [2,2])

#BPP
metrics = execute_algorithm("BPP", root, objective_state, None)

#HEUR_GLOBAL
#metrics = execute_algorithm("HEUR_GLOBAL", root, objective_state, total_squares)

#HEUR_LOCAL   with backtracking
#metrics = execute_algorithm("HEUR_LOCAL", root, objective_state, total_squares)

#A*
#metrics = execute_algorithm("A*", root, objective_state, total_squares)

print("Status: {0}".format("success" if metrics.solved else "failure"))
print("Depth: {0}".format(metrics.depth))
print("Nodes expanded: {0}".format(metrics.expanded))
print("Nodes in frontier: {0}".format(metrics.frontier))
if metrics.solution != None:
    print("Solution:\n")
    for board in metrics.solution:
        for row in board:
            print(row)
        print()
print("Time: {0} s".format(metrics.time, '{0:.2f}'))


