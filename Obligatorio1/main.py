from models import Properties
from solver import solve
from io_parser import  parse_properties,generate_output


def __main__():

    properties:Properties = parse_properties()

    #Execute the algorithm based on the properties
    metrics = solve(properties)

    #Process metrics for data visualization
    generate_output(metrics,properties)
    
if __name__ == "__main__":
    __main__()