import math

class Metrics:
    def __init__(self,method,error,x,time):
        self.time = time
        self.error = error
        self.x = x
        self.method = method

class Properties:
    def __init__(self,initial_values,initial_results):
        self.initial_values = initial_values
        self.initial_results = initial_results

class Function:
    def __init__(self,initial_values,initial_results):
        self.initial_values = initial_values
        self.initial_results = initial_results
    
    def logistic_fun(self,val):
        try:
            return math.exp(val) / (1 + math.exp(val))
        except:
            return 1

    def F(self,W,w,w0,epsilon):

        external_sum = 0
        for i in range(0,2):
            internal_sum = 0
            for j in range(0,3):
                internal_sum += w[i][j] * epsilon[j]
            internal_sum -= w0[i]
            external_sum+= W[i+1] * self.logistic_fun(internal_sum)
        return self.logistic_fun(external_sum - W[0])


    def error(self,x,step):

        W = x[0:3]
        w = [x[3:6],x[6:9]]
        w0 = x[9:11]

        sum = 0

        for i in range(0,len(self.initial_results)):
            sum += math.pow(self.initial_results[i] - self.F(W,w,w0,self.initial_values[i]),2)    
        return sum