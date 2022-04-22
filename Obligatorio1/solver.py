import math, time
from scipy.optimize import minimize
from autograd import grad
import numdifftools as nd
from autograd.misc.optimizers import adam,sgd
import numpy as np
from models import Properties, Metrics


def logistic_fun(val):
    try:
        return math.exp(val) / (1 + math.exp(val))
    except:
        return 1

def F(W,w,w0,epsilon):

    external_sum = 0
    for i in range(0,2):
        internal_sum = 0
        for j in range(0,3):
            internal_sum += w[i][j] * epsilon[j]
        internal_sum -= w0[i]
        external_sum+= W[i+1] * logistic_fun(internal_sum)
    return logistic_fun(external_sum - W[0])


def error(x,step):

    W = x[0:3]
    w = [x[3:6],x[6:9]]
    w0 = x[9:11]

    initial_values = [[4.4793,-4.0765,-4.0765],[-4.1793,-4.9218,1.7664],[-3.9429,-0.7689,4.8830]]
    initial_results = [0,1,1]

    sum = 0

    for i in range(0,len(initial_results)):
        sum += math.pow(initial_results[i] - F(W,w,w0,initial_values[i]),2)    
    return sum


def solve(properties:Properties):  
    initial_values = properties.initial_values
    initial_results = properties.initial_results

    metrics = []

    #Definir arreglo de pesos iniciales
    x = np.zeros(11) 

    start = time.perf_counter()
    # Gradiente descendiente
    dg_x = sgd(nd.Gradient(error), x)
    end = time.perf_counter()
    metrics.append(Metrics("DG", error(dg_x,0),dg_x,end-start))
    start = end

    # Gradiente conjugado

    cg_result = minimize(error, x,args=(0), method='CG')

    end = time.perf_counter()
    metrics.append(Metrics("CG",cg_result.fun,cg_result.x, end-start))
    start = end

    #ADAM
    adam_x = adam(nd.Gradient(error),x, step_size=0.80085)
    end = time.perf_counter()
    metrics.append(Metrics("ADAM", error(adam_x,0),adam_x,end-start))

    return metrics