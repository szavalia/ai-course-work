import json
import numpy as np
from letters import get_patterns,get_noise_patterns
from models import HopfieldObservables, HopfieldProperties

def generate_hopfield_results(observables:HopfieldObservables):
    for (index,states) in enumerate(observables.pattern_states):
        file_name = "hopfield_{0}.txt".format(index+1)
        file = open(file_name, "w")
        for state in states:
            state_splits = np.array_split(state,5)
            for state_split in state_splits:
                symbols = []
                for value in state_split:
                    if(value == -1):
                        symbols.append(".")
                    else:
                        symbols.append("*")
                file.write("{0} {1} {2} {3} {4}\n".format(symbols[0], symbols[1], symbols[2], symbols[3], symbols[4]))
            file.write("\n")
        file.close()
        
def generate_hopfield_output(properties:HopfieldProperties,observables:HopfieldObservables):
    print("Method: {0}".format(properties.method))
    print("Patterns: {0}".format(properties.letters))
    print("Noise probability: {0}".format(properties.noise_prob))
    print("See hopfield_n.txt files for results")
    generate_hopfield_results(observables)

def parse_hopfield_properties(json_values):
    hopfield_props = json_values.get("hopfield_props")
    if hopfield_props == None:
        print("Hopfield properties are required")
        exit(-1)
    letters = hopfield_props.get("patterns")
    if letters == None:
        print("Pattern letters are required")
        exit(-1)
    if len(letters) != 4:
        print("Invalid length. 4 pattern letters are required")
        exit(-1)
    patterns = get_patterns(letters)
    noise_prob = hopfield_props.get("noise_prob")
    if noise_prob == None:
        print("Noise probability is required")
        exit(-1)
    noise_patterns = get_noise_patterns(patterns, noise_prob)
    return HopfieldProperties(letters,patterns,noise_prob,noise_patterns)


def parse_properties():
    file = open('config.json')
    json_values = json.load(file)
    file.close()

    method = json_values.get("method")

    if method == None:
        print("Method is required")
        exit(-1)

    if(method == "hopfield"):
        return parse_hopfield_properties(json_values)
    if(method == "kohonen"):
        return None
    
    print("Invalid method")
    exit(-1)
    