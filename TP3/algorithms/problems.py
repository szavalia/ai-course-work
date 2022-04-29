import numpy as np

def denormalize_tanh(max,min,value):
    return (((value+1) * (max-min))/2) + min

def normalize_tanh(max,min,value):
    return (2*(value - min) / (max-min))-1

def denormalize_logistic(max,min,value):
    return (value * (max-min)) + min

def normalize_logistic(max,min,value):
    return (value - min) / (max-min)

def denormalize_identity(max,min,value):
    return value

def parse_simple_entry_file(entry_file):
    training_set = []
    file = open(entry_file)
    lines = file.readlines()

    for i in range(0,len(lines)):
        tokens = lines[i].replace("\n", "").split("   ")
        training_set.append([])
        for token in tokens[1:len(tokens)]:
            training_set[i].append(float(token))
    
    return training_set

def parse_multilayer_entry_file(entry_file):
    training_set = []
    file = open(entry_file)
    lines = file.readlines()

    i = 0
    k = 0
    while i < len(lines):
        training_set.append([])
        for j in range(0,7):
            if(i != len(lines) -1):
                tokens = lines[i].replace(" \n", "").split(" ")
            else:
                tokens = lines[i].split(" ")[:-1]
            for token in tokens[0:len(tokens)]:
                training_set[k].append(int(token))
            i+=1
        k+=1 
    return training_set

def parse_entry_file(entry_file,type):
    if(type == "linear" or type == "non_linear"):
        return parse_simple_entry_file(entry_file)
    elif(type == "multilayer"):
        return parse_multilayer_entry_file(entry_file)

def parse_output_file(output_file, type,sigmoid_type):
    output_set = []
    file = open(output_file)
    lines = file.readlines()

    if(sigmoid_type == "tanh" and type == "non_linear"):
        norm_func = normalize_tanh
        denormalized_func = denormalize_tanh
    elif(sigmoid_type == "logistic" and type == "non_linear"):
        norm_func = normalize_logistic
        denormalized_func = denormalize_logistic
    else:
        denormalized_func = denormalize_identity

    for i in range(0,len(lines)):
        replaced_line = lines[i].replace("   ","")
        output_set.append(float(replaced_line))

    normalized_output_set = None
    if(type == "non_linear"):
        max = np.amax(output_set)
        min = np.amin(output_set)
        normalized_output_set = []
        for value in output_set:
            normalized_output_set.append(norm_func(max,min,value))
    
    return (output_set,normalized_output_set,denormalized_func)

def get_problem_sets(type,problem,sigmoid_type,entry_file=None,output_file=None):
    if (type == "step"):
        if (problem == "AND"):
            return ([[-1,1], [1,-1], [-1,-1], [1,1]], [-1,-1,-1,1], None, denormalize_identity)
        if (problem == "XOR"):
            return ([[-1,1], [1,-1], [-1,-1], [1,1]], [1,1,-1,-1], None, denormalize_identity)
    elif(type == "multilayer"):
        if (problem == "XOR"):
            return ([[-1,1], [1,-1], [-1,-1], [1,1]], [[1],[1],[-1],[-1]], None, denormalize_identity)
        if(problem == "odd_number"):
            output_set = []
            for i in range(0,10):
                if( i%2 == 0):
                    output_set.append([1])
                else:
                    output_set.append([0])
            return(parse_entry_file(entry_file,type), output_set,None,denormalize_identity)
        if(problem == "numbers"):
            output_set = []
            for i in range(0,10):
                output_set.append(np.zeros(10,int))
                output_set[i][i] = 1
            return(parse_entry_file(entry_file,type),output_set,None,denormalize_identity)
    elif(type == "linear" or type == "non_linear"):
        (output_set, normalized_set,denormalize_func) = parse_output_file(output_file,type,sigmoid_type)
        return (parse_entry_file(entry_file,type),output_set,normalized_set,denormalize_func)
    else:
        return (None,None)