from io_parser import parse_properties,generate_output
from models import Properties,Observables
from algorithms.perceptron import execute
def __main__():

    #Parse parameters
    properties:Properties = parse_properties()

    #Execute the algorithm based on the properties
    metrics:Observables = execute(properties)

    #Process metrics for data visualization
    generate_output(properties,metrics)

if __name__ == "__main__":
    __main__()