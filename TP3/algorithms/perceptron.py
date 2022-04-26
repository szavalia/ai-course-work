import numpy as np
import random
from models import Observables, Properties,Perceptron

def execute(properties:Properties):

    perceptron:Perceptron = properties.perceptron

    # Add threshold to training set
    training_set = np.insert(properties.training_set, 0, 1, axis=1)

    w = np.zeros(len(training_set[0]))
    error = 1
    min_error = 2 * len(training_set)
    min_w = np.zeros(len(training_set[0]))
    i = 0

    while error > 0 and i < perceptron.max_iterations:
        # Always pick at random or random until covered whole training set and then random again?
        pos = random.randint(0, len(training_set) - 1)
        entry = training_set[pos]
        h = np.dot(entry, w)
        O = perceptron.function(h)
        delta_w = perceptron.learning_rate * (properties.output_set[pos] - O) * entry
        w += delta_w
        error = calculate_error(perceptron.function,training_set, properties.output_set, w)
        i += 1
        if error < min_error:
            min_error = error
            min_w = w.copy()

    return Observables(min_w,min_error)

def calculate_error(perceptron_function,training_set, output_set, w):
    error = 0
    for i in range(len(training_set)):
        entry = training_set[i]
        h = np.dot(entry, w)
        O = perceptron_function(h)
        error += abs(output_set[i] - O)
    return error