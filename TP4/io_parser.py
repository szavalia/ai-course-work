import json
import numpy as np
from letters import get_patterns,get_noise_patterns
from models import HopfieldProperties

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
    