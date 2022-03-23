class Selection:
    def __init__(self,method,func):
        self.method = method
        self.func = func

class Mutation: 
    def __init__(self,method,func,probability,sigma,a):
        self.method = method
        self.func = func
        self.probability = probability
        self.sigma = sigma
        self.a = a

class Crossbreeding:
    points_number = 0

    def __init__(self,method,func, points_number=0):
        self.method = method
        self.func = func
        points_number = points_number

#The parameters for the running of the genetic algorithm
class Properties:
    def __init__(self, population_size, generations, crossbreeding:Crossbreeding, mutation:Mutation, selection:Selection):
        self.population_size = population_size
        self.generations = generations
        self.crossbreeding = crossbreeding
        self.mutation = mutation
        self.selection = selection

#Member of a population
class Individual:    
    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fitness = 0
        
    def set_fitness(self,fitness):
        self.fitness = fitness

    def __str__(self) -> str:
        return self.chromosome

#The parameters for output processing
class Metrics:
    def __init__(self,individual:Individual,ideal_func):
        self.individual = individual
        self.ideal_func = ideal_func
    