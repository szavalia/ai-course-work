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


# Takes a confusion matrix and calculates the Metrics for the studied_class
def get_metrics(confusion_matrix, studied_class, classes_dictionary):
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

    return {"accuracy": accuracy, "precision": precision, "recall": recall, "f1_score": f1_score, 
     "true_positives_rate": true_positives_rate, "false_positives_rate": false_positives_rate}

"""
expected = ["M","M","M","M","M","M","M","M","N","N","N","N","N","N","D","D","D","D","D","D","D","D","D","D","D","D","D"]
calculated=["M","M","M","M","M","N","N","N","M","M","M","N","N","D","N","N","D","D","D","D","D","D","D","D","D","D","D"]
classes = ["M","N","D"]
classes_dictionary = build_classes_dictionary(classes)
confusion_matrix = get_confusion_matrix(classes, classes_dictionary, expected, calculated)
print(confusion_matrix)
print(get_metrics(confusion_matrix, "D", classes_dictionary))
"""