from models import Observables, Properties
import numpy as np


# Builds mapping class -> int for use in confusion matrix
def build_classes_dictionary(classes):
    dictionary = {}
    index = 0
    for singular_class in classes:
        dictionary[singular_class] = index
        index += 1
    return dictionary


# Takes expected and calculated arrays and the division in classes
def get_confusion_matrix(classes, classes_dictionary, expected, calculated):
    matrix = [[0 for x in range(len(classes))] for y in range(len(classes))]

    for i, result in enumerate(calculated):
        # Rows represent the expected values
        row = classes_dictionary[expected[i]]
        #Columns represent the calculated values
        column = classes_dictionary[calculated[i]]
        
        matrix[row][column] += 1
    return matrix


# Takes the expected and calculated values and each class, then gets metrics for each one
def get_discrete_metrics(expected, calculated, classes):
    classes_dictionary = build_classes_dictionary(classes)
    # TODO: adjust calculated values into classes according to an epsilon
    confusion_matrix = get_confusion_matrix(classes, classes_dictionary, expected, calculated)

    metrics_by_class = {}

    for studied_class in classes:
        index_in_matrix = classes_dictionary[studied_class]
        tp = confusion_matrix[index_in_matrix][index_in_matrix]
        tn = sum(np.diag(confusion_matrix)) - tp
        fp = sum([row[index_in_matrix] for row in confusion_matrix]) - tp
        fn = sum(confusion_matrix[index_in_matrix]) - tp

        accuracy = (tp + tn) / sum(confusion_matrix[index_in_matrix])
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        f1_score = (2 * precision * recall) / (precision + recall)
        true_positives_rate = tp / (tp + fn)
        false_positives_rate = fp / (fp + tn)

        metrics_by_class[studied_class]= {"accuracy": accuracy, "precision": precision, "recall": recall, "f1_score": f1_score, 
     "true_positives_rate": true_positives_rate, "false_positives_rate": false_positives_rate}
     # TODO: turn into an object

    return metrics_by_class


# Get metrics for continuous answer spaces
def get_continuous_metrics(expected, calculated, classes=None):
    # The problem has a continuous answer space
    if classes is None:
        ERROR_THRESHOLD = 0.5 # Every class is separated by ERROR THRESHHOLD
        minval = (min(min(expected), min(calculated))//ERROR_THRESHOLD)*ERROR_THRESHOLD # Gets bottom limit divisible by error threshold
        maxval = ((max(max(expected), max(calculated))+ERROR_THRESHOLD)//ERROR_THRESHOLD)*ERROR_THRESHOLD # Gets top limit divisible by error threshold
        classes = np.arange(minval, maxval, ERROR_THRESHOLD)   
        
        # Adjust values to match those of the classes
        for i in range(0, len(expected)):
            expected[i] = (expected[i]//ERROR_THRESHOLD)*ERROR_THRESHOLD
            calculated[i] = (calculated[i]//ERROR_THRESHOLD)*ERROR_THRESHOLD

    classes_dictionary = build_classes_dictionary(classes)    

    confusion_matrix = get_confusion_matrix(classes, classes_dictionary, expected, calculated)
    return np.sum(np.diag(confusion_matrix))/np.sum(confusion_matrix)

"""
expected = ["M","M","M","M","M","M","M","M","N","N","N","N","N","N","D","D","D","D","D","D","D","D","D","D","D","D","D"]
calculated=["M","M","M","M","M","N","N","N","M","M","M","N","N","D","N","N","D","D","D","D","D","D","D","D","D","D","D"]
classes = ["M","N","D"]
classes_dictionary = build_classes_dictionary(classes)
confusion_matrix = get_confusion_matrix(classes, classes_dictionary, expected, calculated)
print(confusion_matrix)
print(get_metrics(confusion_matrix, "D", classes_dictionary))
"""

