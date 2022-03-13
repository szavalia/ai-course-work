from heuristics import heuristic_chooser,fill_positions
from algorithms.uninformed_algorithms import DFS_search
from algorithms.uninformed_algorithms import VDFS_search
from algorithms.uninformed_algorithms import BFS_search
from algorithms.heuristics_algorithms import local_search
from algorithms.heuristics_algorithms import global_search
from algorithms.heuristics_algorithms import a_star_search
from models import *
from math import factorial

def execute_algorithm(alg, root:Node, objective:State, heuristic, starting_depth):
    if alg == "DFS":
        return DFS_search(root, objective)
    elif alg == "BFS":
        return BFS_search(root, objective)
    elif alg == "VDFS":
        if(starting_depth == None or starting_depth < 0 or starting_depth > (factorial(pow(Board.dim,2)))):
            print("Invalid starting depth")
            return None
        
        return VDFS_search(root, objective, starting_depth)
    elif alg == "HEUR_GLOBAL":
        heuristic_function = heuristic_chooser(heuristic)
        
        if(heuristic_function == None):
            print("Invalid heuristic.Try instead: \n\t- total_squares\n\t- total_manhattan\n\t- total_removing_obstacles")
            return None
        
        fill_positions()
        root.state.heuristic = heuristic_function(root.state)
        return global_search(root, objective, heuristic_function)
    elif alg == "HEUR_LOCAL":
        heuristic_function = heuristic_chooser(heuristic)
        
        if(heuristic_function == None):
            print("Invalid heuristic.Try instead: \n\t- total_squares\n\t- total_manhattan\n\t- total_removing_obstacles")
            return None
        
        fill_positions()
        root.state.heuristic = heuristic_function(root.state)
        return local_search(root, objective, heuristic_function)
    elif alg == "A*":
        heuristic_function = heuristic_chooser(heuristic)
        
        if(heuristic_function == None):
            print("Invalid heuristic.Try instead: \n\t- total_squares\n\t- total_manhattan\n\t- total_removing_obstacles")
            return None
        
        fill_positions()
        root.state.heuristic = heuristic_function(root.state)
        return a_star_search(root, objective, heuristic_function)
    else:
        if(alg == None):
            print("Algorithm missing")
            return None
        print("Invalid algorithm. Try instead: \n\t- DFS\n\t- BFS\n\t- VDFS\n\t- HEUR_GLOBAL\n\t- HEUR_LOCAL\n\t- A*")
        return None