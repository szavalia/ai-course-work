import time
from scipy.optimize import minimize
from autograd import grad
import numdifftools as nd
from autograd.misc.optimizers import adam,sgd
import numpy as np
from models import Function, Properties, Metrics

def solve(properties:Properties):  
    function:Function = Function(properties.initial_values,properties.initial_results)

    metrics = []

    #Definir arreglo de pesos iniciales
    x = np.zeros(11) 

    start = time.perf_counter()
    # Gradiente descendiente
    dg_x = sgd(nd.Gradient(function.error), x)
    end = time.perf_counter()
    metrics.append(Metrics("DG", function.error(dg_x,0),dg_x,end-start))
    start = end

    # Gradiente conjugado

    cg_result = minimize(function.error, x,args=(0), method='CG')

    end = time.perf_counter()
    metrics.append(Metrics("CG",cg_result.fun,cg_result.x, end-start))
    start = end

    #ADAM
    adam_x = adam(nd.Gradient(function.error),x, step_size=0.80085)
    end = time.perf_counter()
    metrics.append(Metrics("ADAM", function.error(adam_x,0),adam_x,end-start))

    return metrics