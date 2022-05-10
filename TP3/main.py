from io_parser import parse_properties,generate_output, save_noise_error
from metrics import get_continuous_metrics, get_discrete_metrics
from models import Properties,Observables
from algorithms.perceptron import cross_validate as simple_cross_validate, execute as simple_execute
from algorithms.multilayer import cross_validate as multi_cross_validate, execute as multi_execute,noise_test

def __main__():

    #Parse parameters
    properties:Properties = parse_properties()

    #Execute the training algorithm based on the properties, then test the algorithm
    if(properties.perceptron.type == "multilayer"):
        if(properties.perceptron.problem != "XOR" and properties.cross_validate):
            observables = multi_cross_validate(properties)
        else:
            observables = multi_execute(properties)
            if(properties.perceptron.problem != "XOR"):
                (errors,probabilities) = noise_test(properties,observables)
                save_noise_error(errors,probabilities)
    else:
        if(properties.perceptron.type != "step" and properties.cross_validate):
            observables = simple_cross_validate(properties)
        else:
            observables = simple_execute(properties)
    #Process metrics for data visualization
    generate_output(properties,observables)
        

if __name__ == "__main__":
    __main__()