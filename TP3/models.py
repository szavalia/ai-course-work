#The parameters for the running of perceptron
class Perceptron:
    def __init__(self,type,learning_rate,max_iterations,problem,function):
        self.type = type
        self.max_iterations = max_iterations
        self.problem = problem
        self.function = function
        self.learning_rate = learning_rate

class Properties:
    def __init__(self,perceptron:Perceptron,training_set,output_set):
        self.perceptron = perceptron
        self.training_set = training_set
        self.output_set = output_set

class Observables:
    def __init__(self,w,error):
        self.w = w
        self.error = error