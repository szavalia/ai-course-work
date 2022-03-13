from numpy import longlong
from models import *
import time
from algorithms.move_maker import expand,get_solution
from collections import deque


def search(type, root:Node, objective):
    frontier = deque([root]) #I'm using a Doubly Ended Queue
    explored = {}
    expanded = 0
    start = time.perf_counter()

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

def VDFS_search(root:Node, objective):
    previous_limit = 0
    current_limit = 1
    explored = {}

    while (True):
        result = search_with_limit("DFS", root, objective, current_limit, explored)
        print("Solved: "+str(result.solved))
        print("Depth: "+str(result.depth))
        # I have passed the solution. Therefore the optimal depth lies between the previous and current limits
        if result.solved:
            return find_depth_bound(root, objective, previous_limit, current_limit, explored)

        # I have not found the solution yet
        else:
            if result.depth < current_limit:
                print("System not solvable!")
                return result # The system is not solvable! Increasing the max depth will not help
                
            previous_limit = current_limit
            current_limit *= 2     


def find_depth_bound(root:Node, objective, lower_bound, upper_bound, explored):
    midpoint = (longlong)((lower_bound + upper_bound)/2)
    result = search_with_limit("DFS", root, objective, midpoint, explored)

    print("Solved: "+str(result.solved) +" Depth: "+str(result.depth)+ " Bounds: "+str(lower_bound) + " - "+str(upper_bound))

    if lower_bound == upper_bound:
        return result

    if not result.solved: # Está a la derecha
        return find_depth_bound(root, objective, midpoint+1, upper_bound, explored) 

    else: # Está a la izquierda
        return find_depth_bound(root, objective, lower_bound, midpoint, explored)



def search_with_limit(type, root:Node, objective, depth_limit, explored):
    frontier = deque([root]) #I'm using a Doubly Ended Queue
    explored = {}
    expanded = 0
    start = time.perf_counter()

    while (len(frontier) != 0):
        
        node = frontier.pop() # This is the LIFO way        

        while (explored.get(str(node.state)) != None):  #If it was explored already, get the next one
            if (len(frontier) == 0):
                end = time.perf_counter()
                print("No nodes in frontier")
                return Metrics(False,expanded,len(frontier),end-start,None,node.depth)  # System is not solvable

            node = frontier.pop() # This is the LIFO way
        

        explored[str(node.state.board)] = node # Mark as explored

        if (node.state == objective): # Success!
            solution = get_solution(node)
            end = time.perf_counter()
            print("Search successful")
            return Metrics(True,expanded,len(frontier),end-start,solution,node.depth) 

        # If I have reached this, it's because I haven't reached the solution but haven't failed yet
        if( node.depth == depth_limit):
            end = time.perf_counter()
            print("Reached depth limit")
            return Metrics(False,expanded,len(frontier),end-start,None,node.depth)

        expand(node, None)  # expand(node, heuristic_function)
        expanded += 1

        for aux_node in node.next:
            if explored.get(str(aux_node.state.board)) == None:
                frontier.append(aux_node)

    end = time.perf_counter()
    print("Frontier empty")
    return Metrics(False,expanded,len(frontier),end-start,None,node.depth)