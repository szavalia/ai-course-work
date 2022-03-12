from models import *
from algorithm_chooser import execute_algorithm
import json

def find_empty_space(layout):
    for (row_index,row) in enumerate(layout):
        for (col_index,square_val) in enumerate(row):
            if(square_val == 0):
                return (row_index,col_index)

def get_objective(dim):
    
    objective = []
    square_val=1
    for i in range(dim):
        row = []
        for j in range(dim):
            row.append(square_val)
            square_val+=1
        objective.append(row)
    objective[dim-1][dim-1] = 0
    return objective

file = open('config.json')
config_values = json.load(file)

#get puzzle layout and generate initial state and root node
layout = config_values["puzzle_layout"]
Board.dim = len(layout)
board = Board(layout, find_empty_space(layout))
initial_state = State(board)
root = Node(initial_state,None,0)

#generate solution state
objective_state = State(Board(get_objective(Board.dim), [Board.dim - 1, Board.dim - 1]))

algorithm = config_values["algorithm"]
heuristic = config_values["heuristics"]

#resolve the puzzle
metrics = execute_algorithm(algorithm,root,objective_state,heuristic)

print("Status: {0}".format("success" if metrics.solved else "failure"))

if metrics.solution != None:
    print("Solution:\n")
    for board in metrics.solution:
        for row in board:
            print(row)
        print()

if(metrics.depth != None):
    print("Depth: {0}".format(metrics.depth))

print("Nodes expanded: {0}".format(metrics.expanded))
print("Nodes in frontier: {0}".format(metrics.frontier))
print("Time: {0} s".format(metrics.time, '{0:.2f}'))


