import json
from algorithms.perceptron_functions import function_chooser 
from algorithms.problems import get_problem_sets
from models import Perceptron,Properties,Metrics

def generate_output(properties:Properties, metrics:Metrics):
    print("w: {0}".format(metrics.w))
    print("Error: {0}".format(metrics.error))


def parse_properties():
    file = open('config.json')
    json_values = json.load(file)
    file.close()    

    perceptron_type = json_values.get("perceptron_type")
    
    if perceptron_type == None:
        print("Perceptron type required")
        exit(-1)

    perceptron_function = function_chooser(perceptron_type)

    if perceptron_function == None:
        print("Invalid type {0}".format(perceptron_type))
    
    learning_rate = json_values.get("learning_rate")

    if learning_rate == None:
        print("Learning rate required")
        exit(-1)

    max_iterations = json_values.get("max_iterations")

    if max_iterations == None:
        print("Max iterations required")
        exit(-1)

    problem = json_values.get("problem")

    if(problem == None):
        print("Problem required")
        exit(-1)

    (training_set, output_set) = get_problem_sets(perceptron_type,problem)

    if(training_set == None or output_set == None):
        print("Invalid problem for perceptron {0}", perceptron_type)

    return Properties(Perceptron(perceptron_type,float(learning_rate),int(max_iterations),problem,perceptron_function),training_set,output_set)
    

