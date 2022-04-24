import numpy as np
import random

def execute(training_set, output_set, learning_rate, max_steps):

    # Add threshold to training set
    training_set = np.insert(training_set, 0, 1, axis=1)

    w = np.zeros(len(training_set[0]))
    error = 1
    min_error = 2 * len(training_set)
    min_w = np.zeros(len(training_set[0]))
    i = 0

    while error > 0 and i < max_steps:
        # Always pick at random or random until covered whole training set and then random again?
        pos = random.randint(0, len(training_set) - 1)
        entry = training_set[pos]
        h = np.dot(entry, w)
        O = np.sign(h)
        delta_w = learning_rate * (output_set[pos] - O) * entry
        w += delta_w
        error = calculate_error(training_set, output_set, w)
        i += 1
        if error < min_error:
            min_error = error
            min_w = w.copy()
        print("Iteration: " + str(i) + " w: " + str(w) + " error: " + str(error))

    return (min_w, min_error)


def calculate_error(training_set, output_set, w):
    error = 0
    for i in range(len(training_set)):
        entry = training_set[i]
        h = np.dot(entry, w)
        O = np.sign(h)
        error += abs(output_set[i] - O)
    return error