from algorithm_chooser import execute_algorithm

def __main__():
    """"
    #Parse parameters
    properties:Properties = parse_properties()
    if properties == None:
        return

    #Execute the algorithm based on the properties
    metrics:Metrics = solve(properties)

    #Process metrics for data visualization
    generate_output(metrics, properties)
    """
    (w, error) = execute_algorithm("ej1", "xor")
    if (error != None):
        print("w: " + str(w))
        print("Error: " + str(error))

if __name__ == "__main__":
    __main__()