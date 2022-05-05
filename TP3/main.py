from io_parser import parse_properties,generate_output
from metrics import get_continuous_metrics, get_discrete_metrics
from models import Properties,Observables
from algorithms.perceptron import cross_validate as simple_cross_validate, execute as simple_execute
from algorithms.multilayer import cross_validate as multi_cross_validate, execute as multi_execute

def __main__():

    #Parse parameters
    properties:Properties = parse_properties()

    #Execute the training algorithm based on the properties, then test the algorithm
    if(properties.perceptron.type == "multilayer"):
        if(properties.perceptron.problem != "XOR"):
            observables = multi_cross_validate(properties, 0.2)
        else:
            observables = multi_execute(properties)
    else:
        if(properties.perceptron.type != "step"):
            observables = simple_cross_validate(properties, 0.2)
        else:
            observables = simple_execute(properties)
    #Process metrics for data visualization
    generate_output(properties,observables)
        

if __name__ == "__main__":
    __main__()