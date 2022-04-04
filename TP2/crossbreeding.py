import random
from models import Crossbreeding, Individual

def simple_crossbreeding(population):
    chrom_length = len(population[0].chromosome)
    random.shuffle(population) #Shuffle in case it is ordered from another step and improve diversity of children 
    children = []
    for i in range(0, len(population)-1, 2):
        parent1 = population[i]
        parent2 = population[i+1]
        index = random.randint(1, chrom_length-1)    #Between 1 and len-1 so as to not create a child equal to parent
        chromosome1 = []
        chromosome2 = []
        for j in range(0, index):
            chromosome1.append(parent1.chromosome[j])
            chromosome2.append(parent2.chromosome[j])
        for j in range(index, chrom_length):
            chromosome1.append(parent2.chromosome[j])
            chromosome2.append(parent1.chromosome[j])
        children.append(Individual(chromosome1))
        children.append(Individual(chromosome2))
    population = population + children
    return population


def multiple_crossbreeding(population):
    chrom_length = len(population[0].chromosome)
    random.shuffle(population) #Shuffle in case it is ordered from another step and imrpove diversity of children 
    children = []

    points_number = Crossbreeding.points_number
    try:
        indexes = random.sample(range(0, chrom_length-1), points_number)  #Here between 0 and len-1 because there are more points afterwards so the children wont equal parent
    except ValueError:
        print('Number of points exceed chromosome length for multiple point crossbreeding')
        exit(-1)
    
    switched = False
    for i in range(0, len(population)-1, 2):
        parent1 = population[i]
        parent2 = population[i+1]
        chromosome1 = []
        chromosome2 = []
        for j in range(0, chrom_length):
            if j in indexes:
                switched = not switched
            if not switched:
                chromosome1.append(parent1.chromosome[j])
                chromosome2.append(parent2.chromosome[j])
            else:
                chromosome1.append(parent2.chromosome[j])
                chromosome2.append(parent1.chromosome[j])
        children.append(Individual(chromosome1))
        children.append(Individual(chromosome2))
    population = population + children
    return population
    

def uniform_crossbreeding(population):
    chrom_length = len(population[0].chromosome)
    random.shuffle(population) #Shuffle in case it is ordered from another step and imrpove diversity of children 
    children = []
    for i in range(0, len(population)-1, 2):
        parent1 = population[i]
        parent2 = population[i+1]
        chromosome1 = []
        chromosome2 = []
        for j in range(0, chrom_length):
            if random.random() >= 0.5:
                chromosome1.append(parent1.chromosome[j])
                chromosome2.append(parent2.chromosome[j])
            else:
                chromosome1.append(parent2.chromosome[j])
                chromosome2.append(parent1.chromosome[j])
        children.append(Individual(chromosome1))
        children.append(Individual(chromosome2))
    population = population + children
    return population

def crossbreeding_chooser(crossbreeding_param):
    if crossbreeding_param == None or crossbreeding_param.get("method") == None:
        print("Crossbreeding method required")
        exit(-1)

    method = crossbreeding_param.get("method")

    if(method == "simple"):
        return Crossbreeding(method, simple_crossbreeding)
    if(method == "multiple"):
        points = crossbreeding_param.get("multiple_point_n")
        if points == None or points <=0:
            print("Specify a positive quantity of points for mutiple crossbreeding")
            exit(-1)
        Crossbreeding.points_number = crossbreeding_param.get("multiple_point_n")
        return Crossbreeding(method, multiple_crossbreeding)
    if(method == "uniform"):
        return Crossbreeding(method, uniform_crossbreeding)
    else:
        print("Incorrect crossbreeding algorithm")
        exit(-1)