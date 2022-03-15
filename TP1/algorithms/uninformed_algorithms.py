import sys
from models import *
import time
from algorithms.move_maker import expand,get_solution
from collections import deque
from math import factorial

def search(type, root:Node, objective):
    start = time.perf_counter()
    frontier = deque([root]) #I'm using a Doubly Ended Queue
    explored = {}
    expanded = 0

    while (len(frontier) != 0):
        if type == "BFS":
            node = frontier.popleft() # The expansion method appends to the end of the list, this is the FIFO way
        elif type == "DFS":
            node = frontier.pop() # This is the LIFO way
        

        while (explored.get(str(node.state.board)) != None):  #If it was explored already, get the next one
            if (len(frontier) == 0):
                end = time.perf_counter()
                return Metrics(False,expanded,len(frontier),end-start)  # System is not solvable

            if type == "BFS":
                node = frontier.popleft() # Move on to the next one, FIFO style
            elif type == "DFS":
                node = frontier.pop() # This is the LIFO way
        

        explored[str(node.state.board)] = node # Mark as explored

        if (node.state == objective): # Success!
            solution = get_solution(node)
            end = time.perf_counter()
            return Metrics(True,expanded,len(frontier),end-start,solution,node.depth) 

        expand(node, None)  # expand(node, heuristic_function)
        expanded += 1

        for aux_node in node.next:
            if explored.get(str(aux_node.state.board)) == None:
                frontier.append(aux_node)

    end = time.perf_counter()
    return Metrics(False,expanded,len(frontier),end-start)

def BFS_search(root:Node, objective):
    return search("BFS", root, objective)

def DFS_search(root:Node, objective):
    return search("DFS", root, objective)

def VDFS_search(root:Node, objective, starting_depth):
    global_start = time.perf_counter()
    max_depth = sys.maxsize * 2
    if (Board.dim < 5):
        max_depth = factorial(Board.dim*Board.dim)  # n*n! state posibilities - problem specific
    current_limit = starting_depth
    if current_limit > max_depth:
        current_limit = max_depth
    lower_bound = 0
    upper_bound = -1
    frontier = [root]
    edge_nodes = []     # For making some cases of future runs more performant
    expanded = [0]      # As array so function with less scope can increment
    possible_solution = {"node": None, "frontier_len": 0}  # What we are asked for in Metrics  

    while True:
        #Check for algorithm end
        if (upper_bound == lower_bound or (upper_bound == lower_bound + 1 and possible_solution["node"] != None)):
            global_end = time.perf_counter()
            return Metrics(True,expanded[0],possible_solution["frontier_len"],global_end-global_start,get_solution(possible_solution["node"]),possible_solution["node"].depth) 
        if (lower_bound >= max_depth and upper_bound == -1):
            global_end = time.perf_counter()
            return Metrics(False,expanded[0],len(frontier),global_end-global_start)

        #Execute single search
        (solved, solved_depth, node, time_spent, new_edge_nodes) = single_VDFS(frontier, objective, current_limit, expanded)
        if (solved):
            possible_solution["node"] = node
            possible_solution["frontier_len"] = len(frontier)

        print("For depth: " + str(current_limit) + ", Solved: " + str(solved) + (" with depth " + str(solved_depth) if solved else "")  + ", Time spent: ", str(format(time_spent,".4f")))

        #New search with new depth
        if (solved):
            upper_bound = solved_depth
            current_limit = (lower_bound + solved_depth) // 2
            frontier.clear()
            frontier.extend(edge_nodes)     #Start from the nodes that didnt expand on run with previous limit
            if (len(frontier) == 0):        #If none, then from root
                frontier.append(root)
        else:
            lower_bound = current_limit
            edge_nodes = new_edge_nodes     #Now we know there are no solutions below this depth, so start from here
            frontier.clear()
            frontier.extend(new_edge_nodes)     #Start from the nodes that didnt expand on run with previous limit
            
            if (upper_bound == -1):
                current_limit = lower_bound * 2
                if (current_limit > max_depth):
                    current_limit = max_depth
            else:
                current_limit = (upper_bound + lower_bound) // 2
                

def single_VDFS(frontier, objective, current_limit, expanded):
    start = time.perf_counter()
    explored = {}
    new_edge_nodes = []

    while (len(frontier) != 0):
        node = frontier.pop()
        
        explored_entry = explored.get(str(node.state.board))
        while (explored_entry != None and explored_entry.depth <= node.depth):  #If it was explored already, get the next one
            if (len(frontier) == 0):
                end = time.perf_counter()
                return (False, None, None, end-start, new_edge_nodes)  # System is not solvable for current depth

            node = frontier.pop()
            explored_entry = explored.get(str(node.state.board))
        

        explored[str(node.state.board)] = node # Mark as explored

        if (node.state == objective): # Success!
            end = time.perf_counter()
            return (True, node.depth, node, end-start, None) 

        if (node.depth < current_limit):
            expand(node, None)  # expand(node, heuristic_function)
            expanded[0] += 1
        else:
            new_edge_nodes.append(node) # For performance in future runs

        for aux_node in node.next:
            explored_entry = explored.get(str(aux_node.state.board))
            if (explored_entry == None or explored_entry.depth > aux_node.depth):
                frontier.append(aux_node)

    end = time.perf_counter()
    return (False, None, None, end-start, new_edge_nodes)
