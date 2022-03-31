from models import Selection
import random,math

def elite_selection(population):
    #Keep the most fit half of individuals
    population.sort(key=lambda individual: individual.fitness, reverse=True)
    del population[(len(population)//2):]
    return population


def truncation_selection(population):
    #Choose at random having first removed the lowest fitness k individuals
    k = Selection.truncation_k
    desired_size = len(population)//2

    population.sort(key=lambda individual: individual.fitness, reverse=True)
    del population[(len(population)-k):]

    random.shuffle(population)
    del population[desired_size:]
    return population


def roulette_selection(population):
    #Probability of being selected is proportional to fitness
    new_pop = []

    #Get total fitness
    total_fitness = 0
    lowest_fitness = population[0].fitness

    for individual in population:
        if(individual.fitness < lowest_fitness):
            lowest_fitness = individual.fitness
    for individual in population:
        total_fitness += individual.fitness - lowest_fitness

    #Fill probabilities
    relative_fitness = []
    probabilities_array = []
    population.sort(key=lambda individual: individual.fitness, reverse=True) #One full sort so as to lower the overall passes over probabilities array (the first ones are the most likely to be chosen if this is done)
    for index, individual in enumerate(population):
        fitness = individual.fitness - lowest_fitness
        relative_fitness.append(fitness/total_fitness)
        probabilities_array.append(sum(relative_fitness[:index+1]))

    #Draw winners
    for i in range(len(population)//2):
        rand = random.random()
        for index, probability in enumerate(probabilities_array):
            if(rand < probability):
                new_pop.append(population[index])
                break

    return new_pop


def rank_selection(population):
    #Probability of being selected is proportional to relative fitness
    new_pop = []

    #Fill probabilities
    population.sort(key=lambda individual: individual.fitness, reverse=True) #Sort to order individuals for rank selection
    probabilities_array = []
    indexes_sum = (len(population) * (len(population)+1))//2
    probabilities_array.append(len(population)/indexes_sum)
    for i in range(1, len(population)):
        new_value = ((len(population) - i)/indexes_sum) + probabilities_array[i-1]
        probabilities_array.append(new_value)

    #Draw winners
    for i in range(len(population)//2):
        rand = random.random()
        for index, probability in enumerate(probabilities_array):
            if(rand < probability):
                new_pop.append(population[index])
                break
	
    return new_pop


def clash(fighter1, fighter2):
    fitter_chance = Selection.tournament_threshold
    outcome = random.random()
    if(fighter1.fitness > fighter2.fitness):
        if(outcome < fitter_chance):    #Fittest wins
            return fighter1
        else:
            return fighter2
    else:
        if(outcome < fitter_chance):    #Fittest wins
            return fighter2
        else:
            return fighter1

def tournament_selection_nr(population):    #No replacement
    #Take a pair at random and make them fight for a spot, with the fittest having more chance of success
    random.shuffle(population)
    new_pop = []
    for i in range(0, len(population)-1, 2):
        fighter1 = population[i]
        fighter2 = population[i+1]
        new_pop.append(clash(fighter1, fighter2))

    return new_pop


def tournament_selection_wr(population):        #With replacement
    #Winner of 4, with replacement
    new_pop = []
    while (len(new_pop) < len(population)/2):
        fighter1 = random.choice(population)
        fighter2 = random.choice(population)
        fighter3 = random.choice(population)
        fighter4 = random.choice(population)
        winner1 = clash(fighter1, fighter2)
        winner2 = clash(fighter3, fighter4)
        new_pop.append(clash(winner1, winner2))
    
    return new_pop


def T(t,Tc,T0,k):
    return Tc + (T0-Tc) * math.exp(-k*t)

def boltzmann_aptitude(individual,t,Tc,T0,k):
    return (math.exp(individual.fitness) / T(t,Tc,T0,k))

def boltzmann_selection(population):
    Tc = Selection.boltzmann_tc
    T0 = Selection.boltzmann_t0
    k = Selection.boltzmann_k
    t = Selection.boltzmann_t

    #Probability of being selected is proportional to fitness
    new_pop = []

    #Get total fitness
    total_fitness = 0
    for individual in population:
        total_fitness += boltzmann_aptitude(individual,t,Tc,T0,k)

    #Fill probabilities
    relative_fitness = []
    probabilities_array = []

    population.sort(key=lambda individual: individual.fitness, reverse=True) #One full sort so as to lower the overall passes over probabilities array (the first ones are the most likely to be chosen if this is done)
    for index, individual in enumerate(population):
        relative_fitness.append(boltzmann_aptitude(individual,t,Tc,T0,k) / total_fitness)
        probabilities_array.append(sum(relative_fitness[:index+1]))

    #Draw winners
    for i in range(len(population)//2):
        rand = random.random()
        for index, probability in enumerate(probabilities_array):
            if(rand < probability):
                new_pop.append(population[index])
                break

    Selection.boltzmann_t = t+1

    return new_pop


def selection_chooser(selection):
    method = selection.get("method")
    if(method == "elite"):
        return Selection(method, elite_selection)
    if(method == "roulette"):
        return Selection(method, roulette_selection)
    if(method == "rank"):
        return Selection(method, rank_selection)
    if(method == "tournament_nr" or method == "tournament_wr"):
        Selection.tournament_threshold = selection.get("tournament_threshold")
        if(method == "tournament_nr"):
            return Selection(method, tournament_selection_nr)
        else:
            return Selection(method, tournament_selection_wr)
    if(method == "truncation"):
        Selection.truncation_k = selection.get("truncation_k")
        return Selection(method, truncation_selection)
    if(method == "boltzmann"):
        Selection.boltzmann_k = selection.get("boltzmann_k")
        Selection.boltzmann_tc = selection.get("boltzmann_tc")
        Selection.boltzmann_t0 = selection.get("boltzmann_t0")
        return Selection(method,boltzmann_selection)
    else:
        print("Incorrect algorithm")
        return None