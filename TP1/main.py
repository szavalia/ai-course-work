from models import *
from heuristics import *
from algorithm_chooser import execute_algorithm

initial_state = State([[1,2,3],[4,5,7],[8,0,6]], [2,1], 0)
#initial_state = State([[1,2,3],[4,5,6],[0,7,8]], [2,0], 0)
root = Node(initial_state,None,0)
objective_state = State([[1,2,3],[4,5,6],[7,8,0]], [2,2], 0)

#BPP
#metrics = execute_algorithm("BPP", root, objective_state, None)

#HEUR_GLOBAL
#metrics = execute_algorithm("HEUR_GLOBAL", root, objective_state, total_squares)

#HEUR_LOCAL   with backtracking
metrics = execute_algorithm("HEUR_LOCAL", root, objective_state, total_squares)

print("Status: " + ("success" if metrics.solved else "failure"))
if metrics.solution != None:
    print("Solution:\n")
    for board in metrics.solution:
        for row in board:
            print(row)
        print()
print("Nodes expanded: " + str(metrics.expanded))
print("Nodes in frontier: " + str(metrics.frontier))
print("Time :" + str(metrics.time))
print("Depth: " + str(metrics.depth))


