from models import OjaProperties,OjaObservables
import numpy as np
import random as rn
import sys
import math

def standardize_input(input_set):
    # Calculates standard deviations and means for each field
    field_set = np.array(input_set).transpose()
    field_aggregations = []
    for field in field_set:
        field_aggregations.append([np.mean(field), np.std(field)])
    
    # Build standardized set
    output_set = []
    for entry in input_set:
        aux_row = []
        for index,field in enumerate(entry):
            aux_row.append((field - field_aggregations[index][0]) / field_aggregations[index][1])
            
        output_set.append(aux_row.copy())
    return output_set
    
def execute(properties:OjaProperties):
    # Initialize input values
    input_set = standardize_input(properties.input_set)
    
    w = np.random.uniform(-1,1,len(input_set[0]))

    for i in range(properties.epochs):
        for input in input_set:
            s = np.dot(input,w)
            w += properties.eta * s * (input- s*w)
    
    principal_component = []
    for input in input_set:
        s = np.dot(input,w)
        principal_component.append(s)
    
    return OjaObservables(principal_component,w)