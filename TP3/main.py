from io_parser import parse_properties,generate_output
from models import Properties,Observables
from algorithms.perceptron import execute as simple_execute
from algorithms.multilayer import execute as multi_execute
def __main__():

    #Parse parameters
    properties:Properties = parse_properties()

    #Execute the algorithm based on the properties
    if(properties.perceptron.type == "multilayer"):
        metrics:Observables = multi_execute(properties)
    else:
        metrics:Observables = simple_execute(properties)

    #Process metrics for data visualization
    generate_output(properties,metrics)

if __name__ == "__main__":
    __main__()