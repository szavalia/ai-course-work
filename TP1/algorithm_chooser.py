from algorithms.uninformed_algorithms import BPP_search
from algorithms.uninformed_algorithms import BPA_search
from algorithms.heuristics_algorithms import local_search
from algorithms.heuristics_algorithms import global_search
from algorithms.heuristics_algorithms import a_star_search

def execute_algorithm(alg, root, state, heuristic_function):
    if alg == "BPP":
        return BPP_search(root, state)
    elif alg == "BPA":
        return BPA_search(root, state)
    elif alg == "HEUR_GLOBAL":
        return global_search(root, state, heuristic_function)
    elif alg == "HEUR_LOCAL":
        return local_search(root, state, heuristic_function)
    elif alg == "A*":
        return a_star_search(root, state, heuristic_function)
    else:
        print("Invalid algorithm. Try instead: \n\t- BPP\n\t- BPA\n\t- BPPV\n\t- HEUR_GLOBAL\n\t- HEUR_LOCAL\n\t- A*")
        return None