from models import *
import time
from algorithms.move_maker import expand

def search(root:Node, objective, heuristic_function):
    frontier = [root] 
    explored = {}
    expanded = 0
    start = time.perf_counter()

    while (len(frontier) != 0):
        node = frontier.pop() 
        explored[str(node.state)] = node
        if (node.state == objective):
            solution = get_solution(node)
            end = time.perf_counter()
            return Metrics(True,expanded,len(frontier),end-start,solution,node.depth) 
        expand(node, heuristic_function)  #node, heuristic_function
        expanded+=1 
        added = False
        for aux_node in node.next:
            if explored.get(str(aux_node.state)) == None:
                frontier.append(aux_node)
                added = True
        if added:
            frontier.sort(key=lambda node: node.state.heuristic, reverse=True)
        
    end = time.perf_counter()
    return Metrics(False,expanded,len(frontier),end-start) 

def get_solution(node:Node):
    solution = []
    aux_node = node
    while aux_node.prev != None:
        solution.insert(0,aux_node.state.board)
        aux_node = aux_node.prev
    return solution



