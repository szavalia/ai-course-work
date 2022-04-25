import time
from scipy.optimize import minimize
import numdifftools as nd
from autograd.misc.optimizers import adam
import numpy as np
from models import Function, Properties, Metrics

def solve(properties:Properties):  
    function:Function = Function(properties.initial_values,properties.initial_results)

    metrics = []

    x = np.zeros(11) 

    start = time.perf_counter()
    
    #Descent gradient
    dg_result = minimize(function.error, x,args=(0), method='BFGS')
    end = time.perf_counter()
    metrics.append(Metrics("DG",dg_result.fun,dg_result.x,end-start))
    start = end

    #Conjugate gradient 
    cg_result = minimize(function.error, x,args=(0), method='CG')

    end = time.perf_counter()
    metrics.append(Metrics("CG",cg_result.fun,cg_result.x, end-start))
    start = end

    #ADAM
    adam_x = adam(nd.Gradient(function.error),x, step_size=0.80085)
    end = time.perf_counter()
    metrics.append(Metrics("ADAM", function.error(adam_x,0),adam_x,end-start))

    return metrics