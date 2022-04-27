import numpy as np

def normalize_tanh(max,min,value):
    return (2*(value - min) / (max-min))-1

def normalize_logistic(max,min,value):
    return (value - min) / (max-min)

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

def parse_output_file(output_file, type,sigmoid_type):
    output_set = []
    file = open(output_file)
    lines = file.readlines()

    if(sigmoid_type == "tanh"):
        norm_func = normalize_tanh
    else:
        norm_func = normalize_logistic

    for i in range(0,len(lines)):
        replaced_line = lines[i].replace("   ","")
        output_set.append(float(replaced_line))

    if(type == "non_linear"):
        max = np.amax(output_set)
        print(max)
        min = np.amin(output_set)
        print(min)
        new_output_set = []
        for value in output_set:
            new_output_set.append(norm_func(max,min,value))
        output_set = new_output_set
    
    print(output_set)
    return output_set

def get_problem_sets(type,problem,sigmoid_type,entry_file=None,output_file=None):
    if (type == "step"):
        if (problem == "AND"):
            return ([[-1,1], [1,-1], [-1,-1], [1,1]], [-1,-1,-1,1])
        if (problem == "XOR"):
            return ([[-1,1], [1,-1], [-1,-1], [1,1]], [1,1,-1,-1])
    elif(type == "linear" or type == "non_linear"):
        return (parse_entry_file(entry_file,type),parse_output_file(output_file,type,sigmoid_type))
    else:
        return (None,None)