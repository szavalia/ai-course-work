import numpy as np
import random
from metrics import get_continuous_metrics
from models import Observables, Properties,Perceptron

def execute(properties:Properties):
    perceptron:Perceptron = build_perceptron(properties)    
    # Add threshold to training set
    training_set = np.insert(properties.training_set, 0, 1, axis=1)

    w = np.zeros(len(training_set[0]))
    error = 1
    min_error = 2 * len(training_set)
    min_w = np.zeros(len(training_set[0]))
    i = 0

    output_set = properties.output_set

    while error > perceptron.min_error and i < perceptron.max_iterations:
        # Always pick at random or random until covered whole training set and then random again?
        pos = random.randint(0, len(training_set) - 1)
        entry = training_set[pos]
        h = np.dot(entry, w)
        O = perceptron.function(h)
        normalized_output = properties.normalized_function(properties.output_max,properties.output_min,properties.sigmoid_max,properties.sigmoid_min,output_set[pos])
        delta_w = perceptron.learning_rate * (normalized_output - O) * entry * perceptron.d_function(h)
        w += delta_w
        error = calculate_error(perceptron.function,training_set, output_set, w,properties)
        i += 1
        if error < min_error:
            min_error = error
            min_w = w.copy()
    
    return Observables(min_w,min_error,i)

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
def get_results(properties:Properties, perceptron:Perceptron, w):
    perceptron = build_perceptron(properties)
    results = []
    input_set = np.insert(properties.training_set, 0, 1, axis=1)

    for entry in input_set:
        h = np.dot(entry, w)
        O = perceptron.function(h)
        denormalized_O = properties.normalized_function(properties.sigmoid_max,properties.sigmoid_min,properties.output_max,properties.output_min,O)
        results.append(denormalized_O)
    
    return results

# Tests perceptron using a given weight vector and gets the metrics for it
def test(properties:Properties, w, metrics_function, classes=None):
    perceptron:Perceptron = build_perceptron(properties)

    results = get_results(properties, perceptron, w)

    metrics = metrics_function(properties.output_set, results, classes)

    return metrics

