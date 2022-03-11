from algorithms.BPP import search as BPP_search
from algorithms.heuristic_global import search as heur_global_search
from algorithms.heuristic_local import search as heur_local_search
from algorithms.a_star import search as a_star_search

def execute_algorithm(alg, root, state, heuristic_function):
    if alg == "BPP":
        return BPP_search(root, state)
    elif alg == "HEUR_GLOBAL":
        return heur_global_search(root, state, heuristic_function)
    elif alg == "HEUR_LOCAL":
        return heur_local_search(root, state, heuristic_function)
    elif alg == "A*":
        return a_star_search(root, state, heuristic_function)
    else:
        print("Invalid algorithm")
        return None