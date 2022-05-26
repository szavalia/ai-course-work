import json
import numpy as np
from letters import get_patterns,get_noise_patterns
from models import HopfieldObservables, HopfieldProperties, KohonenObservables, KohonenProperties, OjaObservables,OjaProperties
import pandas as pd

def generate_hopfield_results(observables:HopfieldObservables):
    for (index,states) in enumerate(observables.pattern_states):
        file_name = "resources/hopfield_{0}.txt".format(index+1)
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

def generate_kohonen_results(properties:KohonenProperties, observables:KohonenObservables):
    with open("resources/classifications.csv", "w") as f:
        f.write("Country,Row,Column\n")
        for country in properties.input_names:
            f.write("{0},{1},{2}\n".format(country[0], observables.classifications.get(country[0]).i, observables.classifications.get(country[0]).j))
    
    with open("resources/u_matrix.csv", "w") as f:
        f.write("Row,Colum,Avg_distance\n")
        for (row_index, col_index) in observables.u_matrix.keys(): 
            f.write("{0},{1},{2}\n".format(row_index,col_index,observables.u_matrix.get((row_index,col_index))))

def generate_kohonen_output(properties:KohonenProperties, observables:KohonenObservables):
    print("Method: {0}".format(properties.method))
    print("Eta: {0}".format(properties.eta))
    print("K: {0}".format(properties.k))
    print("R: {0}".format(properties.r))
    print("Epochs: {0}".format(properties.epochs))
    print("See u_matrix.csv and classifications.csv")
    generate_kohonen_results(properties,observables)

def generate_oja_results(properties:OjaProperties,observables:OjaObservables):
    with open("resources/components.csv", "w") as f:
        f.write("Country,Component\n")
        for (index, country) in enumerate(properties.input_names):
            f.write("{0},{1}\n".format(country,observables.principal_component[index]))
    
    with open("resources/loadings.csv", "w") as f:
        f.write("Variable,Loading\n")
        for (index,loading) in enumerate(observables.loadings):
            f.write("{0},{1}\n".format(index+1, loading))


def generate_oja_output(properties:OjaProperties,observables:OjaObservables):
    print("Method: {0}".format(properties.method))
    print("Eta: {0}".format(properties.eta))
    print("Epochs: {0}".format(properties.epochs))
    print("See component.csv and loadings.csv")
    generate_oja_results(properties,observables)
    

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

def get_countries_dataset(path):
    dataset = pd.read_csv(path, delimiter=",")
    return (dataset.loc[:, dataset.columns == "Country"].values, dataset.loc[:, dataset.columns != "Country"].values) 

def parse_kohonen_properties(json_values):
    kohonen_props = json_values.get("kohonen_props")
    if kohonen_props == None:
        print("Kohonen properties are required")
        exit(-1)
    
    dataset_path = kohonen_props.get("dataset_path")
    if dataset_path == None:
        print("Path for dataset is required")
        exit(-1)
    
    (countries,input_set) = get_countries_dataset(dataset_path)

    eta = kohonen_props.get("eta")
    if eta == None or eta <= 0:
        print("Positive eta required")
        exit(-1)
    
    k = kohonen_props.get("k")
    if k == None or k <= 0:
        print("Positive k is required")
        exit(-1)
    
    r = kohonen_props.get("r")
    if r == None or r <= 0:
        print("Positive r is required")
        exit(-1)
    
    epochs = kohonen_props.get("epochs")
    if epochs == None or epochs <= 0:
        print("Positive epochs is required")
        exit(-1)
    
    return KohonenProperties(countries,input_set,eta,k,r,epochs)

def parse_oja_properties(json_values):
    oja_props = json_values.get("oja_props")
    if oja_props == None:
        print("Oja properties are required")
        exit(-1)
    
    dataset_path = oja_props.get("dataset_path")
    if dataset_path == None:
        print("Path for dataset is required")
        exit(-1)
    
    (countries,input_set) = get_countries_dataset(dataset_path)

    eta = oja_props.get("eta")
    if eta == None or eta <= 0:
        print("Positive eta required")
        exit(-1)

    epochs = oja_props.get("epochs")
    if epochs == None or epochs <= 0:
        print("Positive epochs is required")
        exit(-1)
    
    return OjaProperties(countries,input_set,eta,epochs)

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
        return parse_kohonen_properties(json_values)
    if(method == "oja"):
        return parse_oja_properties(json_values)
    
    print("Invalid method")
    exit(-1)
    