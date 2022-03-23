from models import Selection

def elite_selection(population):
    #Keep the most fit half of infividuals
    population.sort(key=lambda individual: individual.fitness, reverse=True)
    del population[(len(population)//2):]

def selection_chooser(selection):
    if(selection.get("method") == "elite"):
        return Selection(selection.get("method"), elite_selection)
    else:
        print("Incorrect algorithm")
        return None