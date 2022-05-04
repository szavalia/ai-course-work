from io_parser import parse_properties,generate_output
from metrics import get_continuous_metrics, get_discrete_metrics
from models import Properties,Observables
from algorithms.perceptron import cross_validate, execute as simple_execute
from algorithms.perceptron import test as simple_test
from algorithms.multilayer import execute as multi_execute
def __main__():

    #Parse parameters
    properties:Properties = parse_properties()

    #Execute the training algorithm based on the properties, then test the algorithm
    if(properties.perceptron.type == "multilayer"):
        observables:Observables = multi_execute(properties)
    else:
        observables = cross_validate(properties, get_continuous_metrics)

    #Process metrics for data visualization
    generate_output(properties,observables)
        

if __name__ == "__main__":
    __main__()