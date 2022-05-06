from models import Metrics
import numpy as np

#correction of XOR output in order to classify later
def correct_XOR(calculated_set,expected_set):
    classes = [0, 1]
    corrected_calculated_set = []
    corrected_expected_set = []
    for i in range(len(calculated_set)):
        if(calculated_set[i][0] >= 0):
            corrected_calculated_set.append(classes[1])
        else:
            corrected_calculated_set.append(classes[0])
        corrected_expected_set.append(expected_set[i][0])
    return (corrected_expected_set,corrected_calculated_set, classes)

def correct_odd_numbers(calculated_set,expected_set):
    classes = [0, 1]
    corrected_calculated_set = []
    corrected_expected_set = []
    for i in range(len(calculated_set)):
        if(calculated_set[i][0] >= 0.5):
            corrected_calculated_set.append(classes[1])
        else:
            corrected_calculated_set.append(classes[0])
        corrected_expected_set.append(expected_set[i][0])
    return (corrected_expected_set,corrected_calculated_set, classes)

def correct_numbers(calculated_set,expected_set):
    classes = [0,1,2,3,4,5,6,7,8,9]
    corrected_calculated_set = []
    corrected_expected_set = []
    for i in range(len(calculated_set)):
        max_index = np.where(calculated_set[i] == np.max(calculated_set[i]))[0][0]
        corrected_calculated_set.append(classes[max_index])
        max_expected_index = np.where(expected_set[i] == np.max(expected_set[i]))[0][0]
        corrected_expected_set.append(classes[max_expected_index])
    return (corrected_expected_set,corrected_calculated_set, classes)

def correct_results(problem,calculated_set,expected_set):
    if(problem == "XOR"):
        return correct_XOR(calculated_set, expected_set)
    if(problem == "odd_number"):
        return correct_odd_numbers(calculated_set, expected_set)
    if(problem == "numbers"):
        return correct_numbers(calculated_set,expected_set)

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
def get_discrete_metrics(expected, calculated, problem):
    (corrected_expected,corrected_calculated,classes) = correct_results(problem,calculated,expected)
    classes_dictionary = build_classes_dictionary(classes)
    confusion_matrix = get_confusion_matrix(classes, classes_dictionary,corrected_expected, corrected_calculated)

    metrics_by_class = []

    for studied_class in classes:
        index_in_matrix = classes_dictionary[studied_class]
        tp = confusion_matrix[index_in_matrix][index_in_matrix]
        tn = sum(np.diag(confusion_matrix)) - tp
        fp = sum([row[index_in_matrix] for row in confusion_matrix]) - tp
        fn = sum(confusion_matrix[index_in_matrix]) - tp
        
        accuracy = (tp + tn) / sum(confusion_matrix[index_in_matrix])
        if (tp == 0 and fp == 0):
            precision = 0
        else:
            precision = tp / (tp + fp)
        if(tp == 0 and fn == 0):
            recall = 0
        else:
            recall = tp / (tp + fn)

        if precision + recall == 0:
            f1_score = 0
        else:
            f1_score = (2 * precision * recall) / (precision + recall)
        if tp + fn == 0:
            true_positives_rate = 0
        else:
            true_positives_rate = tp / (tp + fn)
        if fp + tn == 0:
            false_positives_rate = 0
        else:
            false_positives_rate = fp / (fp + tn)

        metrics = Metrics(accuracy,precision,recall,f1_score,true_positives_rate,false_positives_rate,studied_class)
        metrics_by_class.append(metrics)

    return metrics_by_class


# Get metrics for continuous answer spaces, the field problem is added for compatibility's sake
def get_continuous_metrics(expected, calculated, problem=None):
    # The problem has a continuous answer space
    ERROR_THRESHOLD = 1 # Every class is separated by ERROR THRESHHOLD
    
    hitcount = 0
    # Adjust values to map onto those of the classes
    for i in range(0, len(expected)):
        if abs(expected[i]-calculated[i]) < ERROR_THRESHOLD:
            hitcount += 1

    return Metrics(accuracy=hitcount/len(expected))
