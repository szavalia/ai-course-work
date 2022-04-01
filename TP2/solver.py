from constants import MIN_GENERATIONS
from models import *
import random, math, time

def generate_population(population_size, limit_first_generation):
    #Generate initial population
    limit = limit_first_generation
    population = []

    for i in range(0, population_size):
        population.append(Individual([random.uniform(-limit,limit), random.uniform(-limit,limit), \
            random.uniform(-limit,limit), random.uniform(-limit,limit), random.uniform(-limit,limit), \
            random.uniform(-limit,limit), random.uniform(-limit,limit), random.uniform(-limit,limit), \
            random.uniform(-limit,limit), random.uniform(-limit,limit), random.uniform(-limit,limit), ]))
    
    return population

def logistic_fun(val):
    try:
        return math.exp(val) / (1 + math.exp(val))
    except:
        return 1

def F(W,w,w0,epsilon):

    external_sum = 0
    for i in range(0,1):
        internal_sum = 0
        for j in range(0,2):
            internal_sum += w[i][j] * epsilon[j]
        internal_sum -= w0[i]
        external_sum+= W[i+1] * logistic_fun(internal_sum)
    return logistic_fun(external_sum - W[0])

def calculate_aptitude(individual:Individual,initial_values,initial_results):

    W = individual.chromosome[0:3]
    w = [individual.chromosome[3:6],individual.chromosome[6:9]]
    w0 = individual.chromosome[9:11]

    sum = 0

    for i in range(0,len(initial_results) - 1):
        sum += math.pow(initial_results[i] - F(W,w,w0,initial_values[i]),2)
    
    individual.fitness = -sum


def solve(properties:Properties):  
    start = time.perf_counter()
    max_fitnesses = []
    min_fitnesses = []
    max_fitness_curr = float('-inf')        #Starting values
    min_fitness_curr = 0

    #Generate initial individuals
    population = generate_population(properties.population_size, properties.limit_first_generation)

    #Calculate fitness
    for individual in population:
        calculate_aptitude(individual,properties.initial_values,properties.initial_results)
        if (individual.fitness > max_fitness_curr):
            max_fitness_curr = individual.fitness
        if (individual.fitness < min_fitness_curr):
            min_fitness_curr = individual.fitness
    max_fitnesses.append(max_fitness_curr)
    min_fitnesses.append(min_fitness_curr)
    max_fitness_curr = float('-inf')
    min_fitness_curr = 0

    generations = 1

    while (generations < properties.generations and abs(max_fitnesses[generations-1]) > properties.error_threshold):
        #Crossbreeding
        population = properties.crossbreeding.func(population)

        #Mutation
        population = properties.mutation.func(population, properties.mutation)

        #Calculate fitness
        for individual in population:
            calculate_aptitude(individual,properties.initial_values,properties.initial_results)

        #Selection
        population = properties.selection.func(population)

        for individual in population:
            if (individual.fitness > max_fitness_curr):
                max_fitness_curr = individual.fitness
            if (individual.fitness < min_fitness_curr):
                min_fitness_curr = individual.fitness
        max_fitnesses.append(max_fitness_curr)
        min_fitnesses.append(min_fitness_curr)
        max_fitness_curr = float('-inf')
        min_fitness_curr = 0
  
        generations+=1
        
    population.sort(key=lambda individual: individual.fitness, reverse=True)
    

    W = population[0].chromosome[0:3]
    w = [population[0].chromosome[3:6],population[0].chromosome[6:9]]
    w0 = population[0].chromosome[9:11]

    F_values = []
    for epsilon in properties.initial_values:
        F_values.append(F(W,w,w0,epsilon))
    end = time.perf_counter()

    return Metrics(population[0],F_values,generations, end-start,max_fitnesses,min_fitnesses)
