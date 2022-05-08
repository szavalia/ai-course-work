import numpy as np
import random
from models import Observables, Properties,Perceptron
from io_parser import generate_output, save_error
import sys 

def execute(properties:Properties):
    perceptron:Perceptron = build_perceptron(properties)    
    # Add threshold to training set
    BIAS = 1
    training_set = np.insert(properties.training_set, 0, BIAS, axis=1)
    w = np.zeros(len(training_set[0]))
    error = sys.maxsize
    min_error = sys.maxsize #2 * len(training_set)
    min_w = np.zeros(len(training_set[0]))

    output_set = properties.output_set

    i = len(training_set)
    indexes = []
    epochs = -1
    while error > perceptron.min_error and epochs < perceptron.max_epochs:
        # Always pick at random or random until covered whole training set and then random again?
        #pos = random.randint(0, len(training_set) - 1)
        if(i == len(training_set)):
            epochs+=1
            if not properties.cross_validate and not properties.perceptron.type == "step":
                save_error(epochs, min_error, len(training_set))
            indexes = random.sample(list(range(len(training_set))),len(list(range(len(training_set)))))
            i = 0
        pos = indexes[i]
        entry = training_set[pos]
        h = np.dot(entry, w)
        O = perceptron.function(h)
        normalized_output = properties.normalized_function(properties.output_max,properties.output_min,properties.sigmoid_max,properties.sigmoid_min,output_set[pos])
        delta_w = perceptron.learning_rate * (normalized_output - O) * entry * perceptron.d_function(h)
        w += delta_w
        error = calculate_error(perceptron.function,training_set, output_set, w,properties)

        if error < min_error:
            min_error = error
            min_w = w.copy()
        i+=1
    
    return Observables(min_w,min_error,epochs)

def calculate_error(perceptron_function,training_set, output_set, w,properties:Properties):
    error = 0
    for i in range(len(training_set)):
        entry = training_set[i]
        h = np.dot(entry, w)
        O = perceptron_function(h)
        denormalized_O = properties.normalized_function(properties.sigmoid_max,properties.sigmoid_min,properties.output_max,properties.output_min,O)
        error += (output_set[i] - denormalized_O)**2
    return error*(1/2)

def build_perceptron(properties:Properties):
    perceptron = properties.perceptron

    if(perceptron.type == "non_linear" and perceptron.sigmoid_type == "tanh"):
        properties.sigmoid_max = 1
        properties.sigmoid_min = -1
        properties.output_max = np.max(properties.output_set)
        properties.output_min = np.min(properties.output_set)
    elif(perceptron.type == "non_linear" and perceptron.sigmoid_type == "logistic"):
        properties.sigmoid_max = 1
        properties.sigmoid_min = 0
        properties.output_max = np.max(properties.output_set)
        properties.output_min = np.min(properties.output_set)
    
    return perceptron

# Runs the perceptron with its training_set and returns the result set
def get_results(properties:Properties, w):
    perceptron = build_perceptron(properties)
    results = []
    input_set = np.insert(properties.training_set, 0, 1, axis=1)
    error = 0
    
    for i, entry in enumerate(input_set):
        h = np.dot(entry, w)
        O = perceptron.function(h)
        denormalized_O = properties.normalized_function(properties.sigmoid_max,properties.sigmoid_min,properties.output_max,properties.output_min,O)
        error += (1/2)*(properties.output_set[i]-denormalized_O)**2
        results.append(denormalized_O)

    return (results, error)

# Tests perceptron using a given weight vector and gets the metrics for it
def test(properties:Properties, w, metrics_function):
    (results, error) = get_results(properties, w)

    metrics = metrics_function(properties.output_set, results, properties.perceptron.problem)

    return (metrics, error)


def cross_validate(properties:Properties):
    # Split input into chunks
    # ATTENTION! This product should be an integer in order not to lose entries
    segment_members = int(len(properties.training_set)*properties.test_proportion)
    segment_count = int(1/properties.test_proportion)
    sets = np.array_split(properties.training_set, segment_count)

    max_accuracy = -1
    best_run = None
    original_input = properties.training_set.copy()
    original_output = properties.output_set.copy()

    for k in range(0, segment_count):
        # Build datasets by splitting into testing and training segments
        test_set = sets[k]
        test_output_set = properties.output_set[k*segment_members:(k+1)*segment_members]
        training_set = []
        training_output_set = []
        for i in range(0, segment_members*segment_count):
            if not (i >= k*segment_members and i < (k+1)*segment_members):
                training_set.append(properties.training_set[i])
                training_output_set.append(properties.output_set[i])       
        
        # Train the neural network
        properties.training_set = training_set
        properties.output_set = training_output_set
        observables = execute(properties)

        # Test the neural network
        properties.training_set = test_set
        properties.output_set = test_output_set
        (observables.metrics, observables.test_error) = test(properties, observables.w, properties.metrics_function)
        
        # Update best run
        if observables.metrics.accuracy > max_accuracy:
            max_accuracy = observables.metrics.accuracy
            best_run = observables

        # Reset data
        properties.training_set = original_input
        properties.output_set = original_output

    return best_run        

    
