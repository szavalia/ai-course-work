from constants import MIN_GENERATIONS
from crossbreeding import crossbreeding_chooser
from selection import selection_chooser
from models import Metrics, Properties, Selection, Crossbreeding, Mutation
from selection import selection_chooser
from mutation import mutation_chooser
import json

def write_maxs_mins(path,metrics:Metrics):
    file = open(path+".csv",'w')
    for i in range(metrics.generations):
        file.write(str(metrics.min_fitnesses[i]) + "," + str(metrics.max_fitnesses[i]) + "\n")

def generate_output(metrics:Metrics,properties:Properties):
    print("First population's allele values: [-{0}, {0}]".format(properties.limit_first_generation))
    print("Population's size: {0}".format(properties.population_size))
    print("Generations limit: {0}".format(properties.generations))
    if(properties.error_threshold != -1):
        print("Error Threshold: {0}".format(properties.error_threshold))
    if (properties.crossbreeding.method == "multiple"):
        print("Crossbreeding: {0} with {1} points".format(properties.crossbreeding.method, properties.crossbreeding.points_number))
    else:
        print("Crossbreeding: {0}".format(properties.crossbreeding.method))

    if (properties.mutation.method == "normal"):
        print("Mutation: {0}, probability: {1}, sigma: {2}".format(properties.mutation.method, properties.mutation.probability, properties.mutation.sigma))
    else:
        print("Mutation: {0}, p: {1}, a: {2}".format(properties.mutation.method, properties.mutation.probability, properties.mutation.a))
    
    if (properties.selection.method == "tournament_wr" or properties.selection.method == "tournament_nr" ):
        print("Selection: {0}, threshold: {1}".format(properties.selection.method, properties.selection.tournament_threshold))
    else:
        if (properties.selection.method == "truncation"):
            print("Selection: {0}, k: {1}".format(properties.selection.method, properties.selection.truncation_k))
        else:
            if (properties.selection.method == "boltzmann"):
                print("Selection: {0}, t0: {1}, tc: {2}, k: {3}".format(properties.selection.method, properties.selection.boltzmann_t0, properties.selection.boltzmann_tc, properties.selection.boltzmann_k))
            else:
                print("Selection: {0}".format(properties.selection.method))

    print("W: {0}\nw: {1}\nw0: {2}".format(metrics.individual.chromosome[0:3],[metrics.individual.chromosome[3:6], metrics.individual.chromosome[6:9]],metrics.individual.chromosome[9:11] ))
    print("Func val:[")
    for (index,value) in enumerate(metrics.ideal_func):
        print("     E{0}: {1} ".format(index+1,value))
    print("]")
    print("Error val: {0}".format(abs(metrics.individual.fitness)))
    print("Generations: {0}".format(metrics.generations))
    print("Time: {0} s".format(metrics.time,".4f"))
    write_maxs_mins(properties.output_path,metrics)
    
# Receive parameters from config.json and encapsulate them into properties object
def parse_properties():

    file = open('config.json')
    json_values = json.load(file)
    file.close()    
    
    initial_values = json_values.get("initial_values")
    
    if initial_values == None:
        print("Initial values required")
        exit(-1)
    initial_results = json_values.get("initial_results")
    
    if initial_results == None:
        print("Initial results required")
        exit(-1)
    for result in initial_results:
        if(result !=0 and result != 1):
            print("Invalid initial result. Only 1 or 0 is accepted")
            exit(-1)

    limit_first_generation = json_values.get("limit_first_generation")
    if limit_first_generation == None:
        print("Limit for first generation required")
        exit(-1)
    elif limit_first_generation <= 0:
        print("Specify a positive limit for first generation")
        exit(-1)

    population_size = json_values.get("population_size")
    if population_size == None:
        print("Population size required")
        exit(-1) 
    elif population_size <= 0:
        print("Specify a positive population size")
        exit(-1)

    generations = json_values.get("generations") 
    if generations == None or generations <= 0 or generations < MIN_GENERATIONS:
        generations = MIN_GENERATIONS
        
    error_threshold = json_values.get("error_threshold")
    if(error_threshold == None):
        error_threshold = -1

    output_path = json_values.get("output_path")
    if output_path == None:
        print("Output path required")
        exit(-1)

    selection = selection_chooser(json_values.get("selection"),population_size)

    mutation = mutation_chooser(json_values.get("mutation"))

    crossbreeding = crossbreeding_chooser(json_values.get("crossbreeding"))

    return Properties(initial_values,initial_results,limit_first_generation,population_size, generations,error_threshold,output_path, crossbreeding, mutation, selection)

