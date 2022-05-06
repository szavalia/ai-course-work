import json
from algorithms.perceptron_functions import function_chooser 
from algorithms.problems import get_problem_sets
from models import Perceptron,Properties,Observables
from constants import DEFAULT_ERROR, MIN_EPOCHS

def generate_output(properties:Properties, observables:Observables):
    print("Perceptron type: {0}".format(properties.perceptron.type))
    if(properties.perceptron.problem != None):
        print("Problem: {0}".format(properties.perceptron.problem))
    if(properties.perceptron.sigmoid_type != None):
        print("Sigmoid type: {0} Beta:{1}".format(properties.perceptron.sigmoid_type, properties.beta))
    print("Learning rate: {0}".format(properties.perceptron.learning_rate))
    print("Max Epochs: {0}".format(properties.perceptron.max_epochs))
    print("w: {0}".format(observables.w))
    print("Error: {0}".format(observables.error))
    print("Epochs: {0}".format(observables.epochs))


def parse_properties():
    file = open('config.json')
    json_values = json.load(file)
    file.close()    

    perceptron_type = json_values.get("perceptron_type")
    
    if perceptron_type == None:
        print("Perceptron type required")
        exit(-1)

    cross_validate = (json_values.get("cross_validate") == "True")

    test_proportion = json_values.get("test_proportion")

    if cross_validate and (test_proportion == None or test_proportion < 0 or test_proportion > 1):
        print("Test proportion required")
        exit(-1)

    sigmoid_type = json_values.get("sigmoid_type")
    beta = json_values.get("beta")
    if perceptron_type == "non_linear" and sigmoid_type == None:
        print("Sigmoid type required")
        exit(-1)
    elif perceptron_type == "non_linear" and beta == None:
        print("Beta required")
        exit(-1)

    if beta != None:
        Properties.beta = beta

    (perceptron_function,perceptron_d_function) = function_chooser(perceptron_type,sigmoid_type)

    if perceptron_function == None:
        print("Invalid type {0}".format(perceptron_type))
    
    learning_rate = json_values.get("learning_rate")

    if learning_rate == None:
        print("Learning rate required")
        exit(-1)

    epochs = json_values.get("max_epochs")
    min_error = json_values.get("min_error")

    if epochs == None and min_error == None:
        print("Max iterations or min error required")
        exit(-1)

    if epochs == None or epochs < 0:
        epochs = MIN_EPOCHS
    
    if min_error == None or min_error < 0:
        min_error = DEFAULT_ERROR

    if(perceptron_type == "step" or perceptron_type == "multilayer"):
        problem = json_values.get("problem")
    else:
        problem = None

    entry_path = json_values.get("entry_file")
    output_path = json_values.get("output_file")

    if((type == "linear" or type == "non_linear") and (entry_path == None or output_path == None)):
        print("Entry/Output file required")
        exit(-1)

    (training_set, output_set, normalize_function, metrics_function) = get_problem_sets(perceptron_type,problem,entry_path,output_path)

    if(training_set == None or output_set == None):
        print("Invalid problem for perceptron {0}", perceptron_type)
        exit(-1)

    hidden_layers = json_values.get("hidden_layers")

    return Properties(Perceptron(perceptron_type,learning_rate,epochs,min_error,problem,perceptron_function,sigmoid_type,perceptron_d_function,hidden_layers),training_set,output_set,normalize_function, metrics_function,cross_validate,test_proportion)
    

