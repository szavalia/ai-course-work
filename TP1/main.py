from models import *
from algorithms.BPP import search

initial_state = State([[7,8,6],[5,4,1],[2,3,0]], [2,2])
root = Node(initial_state,None,0)
metrics = search(root,State([[1,2,3],[4,5,6],[7,8,0]], [2,2]))

print("Status: " + ("success" if metrics.solved else "failure"))
#if metrics.solution != None:
#    print("Solution:\n")
#    for board in metrics.solution:
#        for row in board:
#            print(row)
#        print()
print("Nodes expanded: " + str(metrics.expanded))
print("Nodes in frontier: " + str(metrics.frontier))
print("Time :" + str(metrics.time))
print("Depth: " + str(metrics.depth))


