import numpy as np

def parse_simple_entry_file(entry_file):
    training_set = []
    file = open(entry_file)
    lines = file.readlines()

    for i in range(0,len(lines)):
        tokens = lines[i].split("   ")
        training_set.append([])
        for token in tokens[1:len(tokens)]:
            training_set[i].append(float(token))
    
    return training_set

def parse_entry_file(entry_file,type):
    if(type == "linear" or type == "non_linear"):
        return parse_simple_entry_file(entry_file)

def parse_output_file(output_file, type):
    output_set = []
    file = open(output_file)
    lines = file.readlines()

    for i in range(0,len(lines)):
        replaced_line = lines[i].replace("   ","")
        output_set.append(float(replaced_line))

    if(type == "non_linear"):
        max = np.amax(output_set)
        min = np.amin(output_set)
        new_output_set = []
        for value in output_set:
            new_output_set.append((2*(value - min) / (max-min))-1)
        output_set = new_output_set
    
    return output_set

def get_problem_sets(type,problem,entry_file=None,output_file=None):
    if (type == "step"):
        if (problem == "AND"):
            return ([[-1,1], [1,-1], [-1,-1], [1,1]], [-1,-1,-1,1])
        if (problem == "XOR"):
            return ([[-1,1], [1,-1], [-1,-1], [1,1]], [1,1,-1,-1])
    elif(type == "linear" or type == "non_linear"):
        return (parse_entry_file(entry_file,type),parse_output_file(output_file,type))
    else:
        return (None,None)