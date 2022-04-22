#The parameters for output processing
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