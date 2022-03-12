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
        if type == "BPA":
            node = frontier.popleft() # The expansion method appends to the end of the list, this is the FIFO way
        elif type == "BPP":
            node = frontier.pop() # This is the LIFO way
        

        while (explored.get(str(node.state.board)) != None):  #If it was explored already, get the next one
            if (len(frontier) == 0):
                end = time.perf_counter()
                return Metrics(False,expanded,len(frontier),end-start)  # System is not solvable

            if type == "BPA":
                node = frontier.popleft() # Move on to the next one, FIFO style
            elif type == "BPP":
                node = frontier.pop() # This is the LIFO way
        

        explored[str(node.state.board)] = node # Mark as explored

        if (node.state == objective): # Success!
            solution = get_solution(node)
            end = time.perf_counter()
            return Metrics(True,expanded,len(frontier),end-start,solution,node.depth) 

        expand(node, None)  # expand(node, heuristic_function)
        expanded+=1 
        for aux_node in node.next:
            if explored.get(str(aux_node.state.board)) == None:
                frontier.append(aux_node)

    end = time.perf_counter()
    return Metrics(False,expanded,len(frontier),end-start)

def BPA_search(root:Node, objective):
    return search("BPA", root, objective)

def BPP_search(root:Node, objective):
    return search("BPP", root, objective)




