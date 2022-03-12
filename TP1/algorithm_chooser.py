from heuristics import heuristic_chooser,fill_positions
from algorithms.uninformed_algorithms import BPP_search
from algorithms.uninformed_algorithms import BPA_search
from algorithms.heuristics_algorithms import local_search
from algorithms.heuristics_algorithms import global_search
from algorithms.heuristics_algorithms import a_star_search
from models import *

def execute_algorithm(alg, root:Node, objective:State, heuristic):
    if alg == "DFS":
        return BPP_search(root, objective)
    elif alg == "BFS":
        return BPA_search(root, objective)
    elif alg == "HEUR_GLOBAL":
        heuristic_function = heuristic_chooser(heuristic)
        fill_positions(root.state.board)
        root.state.heuristic = heuristic_function(root.state)
        return global_search(root, objective, heuristic_function)
    elif alg == "HEUR_LOCAL":
        heuristic_function = heuristic_chooser(heuristic)
        fill_positions(root.state.board)
        root.state.heuristic = heuristic_function(root.state)
        return local_search(root, objective, heuristic_function)
    elif alg == "A*":
        heuristic_function = heuristic_chooser(heuristic)
        fill_positions(root.state.board)
        root.state.heuristic = heuristic_function(root.state)
        return a_star_search(root, objective, heuristic_function)
    else:
        print("Invalid algorithm. Try instead: \n\t- DFS\n\t- BFS\n\t- BPPV\n\t- HEUR_GLOBAL\n\t- HEUR_LOCAL\n\t- A*")
        return None