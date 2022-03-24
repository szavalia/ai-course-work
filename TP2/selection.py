from models import Selection
import random

def elite_selection(population):
    #Keep the most fit half of individuals
    population.sort(key=lambda individual: individual.fitness, reverse=True)
    del population[(len(population)//2):]
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
    if(method == "tournament"):
        Selection.tournament_threshold = tournament_threshold
        return Selection(method, tournament_selection)
    else:
        print("Incorrect algorithm")
        return None