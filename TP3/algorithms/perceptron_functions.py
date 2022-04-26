from tokenize import String
import numpy as np

def step_perceptron(h):
    return np.sign(h)

def function_chooser(type:String):
    if(type=="step"):
        return step_perceptron
    else:
        return None


