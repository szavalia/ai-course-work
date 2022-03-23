from models import *
from solver import solve
from io_parser import generate_output, parse_properties


def __main__():
    #Parse parameters
    properties:Properties = parse_properties()
    if properties == None:
        return

    #Execute the algorithm based on the properties
    metrics:Metrics = solve(properties)

    #Process metrics for data visualization
    generate_output(metrics, properties)

if __name__ == "__main__":
    __main__()