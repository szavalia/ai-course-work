from tokenize import String
import numpy as np
import math

from models import Properties

def logistic_fun(h):
    try:
        return 1 / (1 + math.exp(-2 * Properties.beta * h))
    except:
        return 1

def step_function(h):
    return np.sign(h)

def linear_function(h):
    return h

def tanh(h):
    return np.tanh(Properties.beta*h)

def d_tanh(h):
    return Properties.beta*(1-(tanh(h)**2))

def d_logistic(h):
    return 2*Properties.beta*logistic_fun(h)*(1-logistic_fun(h))

def d_identity(h):
    return 1

def non_linear_function_chooser(sigmoid_type):
    if(sigmoid_type == "tanh"):
        return (tanh,d_tanh)
    elif(sigmoid_type == "logistic"):
        return (logistic_fun,d_logistic)
    else:
        return None

def function_chooser(type:String,sigmoid_type:String=None):
    if(type=="step"):
        return (step_function,d_identity)
    elif(type=="linear"):
        return (linear_function,d_identity)
    elif(type=="non_linear"):
        return non_linear_function_chooser(sigmoid_type)
    else:
        return None


