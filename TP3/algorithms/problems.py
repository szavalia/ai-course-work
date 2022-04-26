def get_problem_sets(type,problem):
    if (type == "step"):
        if (problem == "AND"):
            return ([[-1,1], [1,-1], [-1,-1], [1,1]], [-1,-1,-1,1])
        if (problem == "XOR"):
            return ([[-1,1], [1,-1], [-1,-1], [1,1]], [1,1,-1,-1])
    else:
        return (None,None)