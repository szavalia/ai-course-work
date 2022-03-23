from models import Mutation
import random

def normal_mutation(population, mutation:Mutation):
    if population == None or mutation == None:
        print("No population provided for mutation, exiting")
        exit(-1)

    for individual in population:

        for x in individual.chromosome:
            #random() returns a value between 0.0 and 1.0
            r = random.random()
            if r < mutation.probability:
                x += random.gauss(0, mutation.sigma)
                print("Mutando con " + str(r) + " -> "+ str(x))

    print("ADENTRO")
    for x in population[0].chromosome:
        print(x)
    
    return population
        
        
def uniform_mutation(population, mutation:Mutation):
    if population == None or mutation == None:
        print("No population provided for mutation, exiting")
        exit(-1)
    
    for individual in population:

        for x in individual.chromosome:
            #random() returns a value between 0.0 and 1.0
            if random.random() < mutation.probability:
                x += random.uniform(-mutation.a, mutation.a)
                
    return population


def mutation_chooser(mutation):
    if mutation == None or mutation.get("method") == None:
        print("Please specify a mutation strategy")
        exit(-1)

    if mutation.get("probability") == None or mutation.get("probability") <= 0:
        print("Please specify a positive mutation probability")

    if mutation.get("method") == "normal":
        if mutation.get("sigma") == None or mutation.get("sigma") < 0:
            print("Sigma must be a positive number")
            exit(-1)
        #Normal mutation strategy with sigma and probability parameters
        return Mutation(mutation.get("method"), normal_mutation, mutation.get("probability"), mutation.get("sigma"), None)
    
    elif mutation.get("method") == "uniform":
        if mutation.get("a") == None or mutation.get("a") <= 0:
            print("The value of 'a' must be positive")
            exit(-1)
        #Uniform mutation strategy with 'a' and probability parameters
        return Mutation(mutation.get("method"), uniform_mutation, mutation.get("probability"), None, mutation.get("a"))

    pass