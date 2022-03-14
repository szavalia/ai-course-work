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

def get_inversions(layout):

    aux_layout = []
    for row in layout:
       aux_layout.extend(row)

    total_inv = 0
    for i in range(pow(Board.dim,2) - 1):
        for j in range(i + 1,pow(Board.dim,2)):
            if (aux_layout[j] and aux_layout[i] and aux_layout[i] > aux_layout[j]):
                total_inv+=1
                
    return total_inv

def is_solvable(layout):
    total_inv = get_inversions(layout)

    if(Board.dim % 2 != 0):
        return (total_inv % 2) == 0
    else:
        empty_row_index = Board.dim - find_empty_space(layout)[0]
        if (empty_row_index % 2 == 0):
            return (total_inv % 2) != 0
        else:
            return (total_inv % 2) == 0

def is_valid(layout):
    total_elements = 0
    repeated_elements = {}
    for row in layout:
        if(len(row) != Board.dim):
            return False
        for val in row:
            if(val < 0 or val >= pow(Board.dim,2) or repeated_elements.get(str(val)) != None):
                return False
            else:
                total_elements +=1
                repeated_elements[str(val)] = val
    
    return total_elements == pow(Board.dim,2)

file = open('config.json')
config_values = json.load(file)
file.close()

#get puzzle layout
layout = config_values.get("puzzle_layout")

if(layout == None):
    print("Initial board missing")
    exit(-1)

Board.dim = len(layout)
#validate puzzle layout
if(not is_valid(layout) or not is_solvable(layout)):
    print("Illegal initial board")
    exit(-1)

#generate initial state and root node
board = Board(layout, find_empty_space(layout))
initial_state = State(board)
root = Node(initial_state,None,0)

#generate solution state
objective_state = State(Board(get_objective(Board.dim), [Board.dim - 1, Board.dim - 1]))

algorithm = config_values.get("algorithm")
heuristic = config_values.get("heuristics")
starting_depth = config_values.get("starting_depth")

#resolve the puzzle
metrics = execute_algorithm(algorithm,root,objective_state,heuristic, starting_depth)

if(metrics != None):

    #Initial parameters
    print("Algorithm: {0}".format(algorithm))
    if(algorithm != "DFS" and algorithm != "BFS" and algorithm != "VDFS"):
        print("Heuristic: {0}".format(heuristic))
    if(algorithm == "VDFS"):
        print("Starting depth: {0}".format(starting_depth))
    
    print("Status: {0}".format("success" if metrics.solved else "failure"))

    if(metrics.depth != None):
        print("Depth: {0}".format(metrics.depth))
    print("Nodes expanded: {0}".format(metrics.expanded))
    print("Nodes in frontier: {0}".format(metrics.frontier))
    print("Time: {0} s".format(str(format(metrics.time,".4f"))))

    if metrics.solution != None:
        print("Solution: see solution.txt")
        
        file = open("solution.txt",'w')

        rows = [[],[],[]]

        for (board_index,board) in enumerate(metrics.solution):
            for row in board:
                file.write("{0}\n".format(str(row)))
            if(board_index != len(metrics.solution) -1):
                file.write("    |\n    |\n    v\n")

        file.close()
else:
    exit(-1)

