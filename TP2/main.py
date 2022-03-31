from models import *
from solver import solve
from io_parser import generate_output, parse_properties, write_maxs_mins


def __main__(run_number):
    #Parse parameters
    properties:Properties = parse_properties()
    if properties == None:
        return

    #Execute the algorithm based on the properties
    metrics:Metrics = solve(properties)

    #Process metrics for data visualization
    generate_output(metrics, properties)
    write_maxs_mins(metrics, run_number)
    
if __name__ == "__main__":
    __main__()