from models import Selection
import random

def elite_selection(population):
    #Keep the most fit half of individuals
    population.sort(key=lambda individual: individual.fitness, reverse=True)
    del population[(len(population)//2):]
    return population

def roulette_selection(population):
    #Probability of being selected is proportional to fitness
    new_pop = []

    #Get total fitness
    total_fitness = 0
    for individual in population:
        total_fitness += individual.fitness

    #Fill probabilities
    relative_fitness = []
    probabilities_array = []
    population.sort(key=lambda individual: individual.fitness, reverse=True) #One full sort so as to lower the overall passes over probabilities array (the first ones are the most likely to be chosen if this is done)
    for index, individual in enumerate(population):
        relative_fitness.append(individual.fitness/total_fitness)
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
    return population

def tournament_selection(population):
    #Take a pair at random and make them fight for a spot, with the fittest having more chance of success
    random.shuffle(population)
    fitter_chance = Selection.tournament_threshold
    new_pop = []
    for i in range(0, len(population)-1, 2):
        fighter1 = population[i]
        fighter2 = population[i+1]
        outcome = random.random()
        if(fighter1.fitness > fighter2.fitness):
            if(outcome < fitter_chance):    #Fittest wins
                new_pop.append(fighter1)
            else:
                new_pop.append(fighter2)
        else:
            if(outcome < fitter_chance):    #Fittest wins
                new_pop.append(fighter2)
            else:
                new_pop.append(fighter1)
    return new_pop


def selection_chooser(selection):
    method = selection["method"]
    tournament_threshold = selection["tournament_threshold"]
    if(method == "elite"):
        return Selection(method, elite_selection)
    if(method == "roulette"):
        return Selection(method, roulette_selection)
    if(method == "rank"):
        return Selection(method, rank_selection)
    if(method == "tournament"):
        Selection.tournament_threshold = tournament_threshold
        return Selection(method, tournament_selection)
    else:
        print("Incorrect algorithm")
        return None