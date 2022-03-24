from models import *
import random,math

def generate_population(population_size):
    #Generate initial population
    limit = 8
    population = []

    for i in range(0, population_size):
        population.append(Individual([random.uniform(-limit,limit), random.uniform(-limit,limit), \
            random.uniform(-limit,limit), random.uniform(-limit,limit), random.uniform(-limit,limit), \
            random.uniform(-limit,limit), random.uniform(-limit,limit), random.uniform(-limit,limit), \
            random.uniform(-limit,limit), random.uniform(-limit,limit), random.uniform(-limit,limit), ]))
    
    return population

def logistic_fun(val):
    return math.exp(val) / (1 + math.exp(val))

def F(W,w,w0,epsilon):

    external_sum = 0
    for i in range(1,2):
        internal_sum = 0
        for j in range(0,2):
            internal_sum += w[i][j] * epsilon[j]
        external_sum+= W[i] * logistic_fun(internal_sum - w0[i])
    return logistic_fun(external_sum - W[0])

def calculate_aptitude(individual:Individual):
    initial_values = [[4.4793,-4.0765,-4.0765],[-4.1793,-4.9218,1.7664],[-3.9429,-0.7689,4.8830]]
    initial_results = [0,1,1]

    W = individual.chromosome[0:3]
    w = [individual.chromosome[3:6],individual.chromosome[6:9]]
    w0 = individual.chromosome[9:11]

    sum = 0

    for i in range(0,2):
        sum += math.pow(initial_results[i] - F(W,w,w0,initial_values[i]),2)
    
    individual.fitness = sum


def solve(properties:Properties):  
    
    #Generate initial individuals
    population = generate_population(properties.population_size)


    generations = 1

    while generations != properties.generations:
        #Crossbreeding
        population = properties.crossbreeding.func(population)

        #Mutation
        population = properties.mutation.func(population, properties.mutation)

        #Calculate fitness
        for individual in population:
            calculate_aptitude(individual)

        #Selection
        population = properties.selection.func(population)

        #Replace old population(already done)
        generations+=1
    
    population.sort(key=lambda individual: individual.fitness, reverse=True)
    
    return Metrics(population[0],0)

