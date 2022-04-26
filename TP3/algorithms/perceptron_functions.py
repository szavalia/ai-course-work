from tokenize import String
import numpy as np
import math

from models import Properties

def logistic_fun(h):
    try:
        return math.exp(2 * Properties.beta * h) / (1 + math.exp(2 * Properties.beta * h))
    except:
        return 1

def step_function(h):
    return np.sign(h)

def linear_function(h):
    return h

def tanh(h):
    return np.tanh(Properties.beta*h)

def non_linear_function_chooser(sigmoid_type):
    if(sigmoid_type == "tanh"):
        return tanh
    elif(sigmoid_type == "logistic"):
        return logistic_fun
    else:
        return None

def function_chooser(type:String,sigmoid_type:String=None):
    if(type=="step"):
        return step_function
    elif(type=="linear"):
        return linear_function
    elif(type=="non_linear"):
        return non_linear_function_chooser(sigmoid_type)
    else:
        return None


