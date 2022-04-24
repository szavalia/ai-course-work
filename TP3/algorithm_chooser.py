import algorithms.ej1 as ej1

def execute_algorithm(ej, prob):
    if (ej == "ej1"):
        if (prob == "and"):
            return ej1.execute([[-1,1], [1,-1], [-1,-1], [1,1]], [-1,-1,-1,1], 0.1, 100)
        if (prob == "xor"):
            return ej1.execute([[-1,1], [1,-1], [-1,-1], [1,1]], [1,1,-1,-1], 0.1, 100)
    print("Invalid algorithm or problem")
    return (None, None)