from models import *
import time
from algorithms.move_maker import expand,get_solution

def search(type, root:Node, objective, heuristic_function):
    frontier = [root] 
    explored = {}
    expanded = 0
    start = time.perf_counter()

    while (len(frontier) != 0):
        node = frontier.pop()
        while (explored.get(str(node.state)) != None):
            if (len(frontier) == 0):
                end = time.perf_counter()
                return Metrics(False,expanded,len(frontier),end-start) 
            node = frontier.pop()
            
        explored[node.state.board_str()] = node

        if (node.state == objective):
            solution = get_solution(node)
            end = time.perf_counter()
            return Metrics(True,expanded,len(frontier),end-start,solution,node.depth) 
            
        expand(node, heuristic_function)  #node, heuristic_function
        expanded+=1 
        added = False
        for aux_node in node.next:
            if explored.get(aux_node.state.board_str()) == None:
                frontier.append(aux_node)
                added = True
        if added:
            if(type == "Local"):
                frontier.sort(key=lambda node: (-node.depth, node.state.heuristic), reverse=True)
            elif(type == "Global"):
                frontier.sort(key=lambda node: node.state.heuristic, reverse=True)
            elif(type == "A*"):
                frontier.sort(key=lambda node: node.state.heuristic + node.depth, reverse=True)
            
    end = time.perf_counter()
    return Metrics(False,expanded,len(frontier),end-start) 

def local_search(root:Node, objective, heuristic_function):
    return search("Local",root,objective,heuristic_function)

def global_search(root:Node, objective, heuristic_function):
    return search("Global",root,objective,heuristic_function)

def a_star_search(root:Node, objective, heuristic_function):
    return search("A*",root,objective,heuristic_function)

