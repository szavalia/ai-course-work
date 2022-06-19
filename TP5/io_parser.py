import json
import numpy as np
from models import Properties,Observables
import fonts
from algorithms.noiser import noise_font

def generate_output(properties:Properties, observables:Observables):
    print("Mode: {0}".format(properties.mode))
    print("Neurons per layer: {0}".format(properties.neurons_per_layer))
    print("Font: {0}".format(properties.font))
    print("Epochs: {0}".format(properties.epochs))
    generate_latent_outputs(observables.latent_outputs,properties.font_chars)
    generate_errors_output(observables.errors_per_step)

def generate_latent_outputs(latent_outputs, font_chars):
    with open("latent.csv", "w") as f:
        f.write("Char,X,Y\n")
        for (i,output) in enumerate(latent_outputs):
            f.write("{0},{1},{2}\n".format(font_chars[i], latent_outputs[i][0], latent_outputs[i][1]))
        
def generate_errors_output(errors):
    with open("errors.csv", "w") as f:
        f.write("Step,Error\n")
        for (i,error) in enumerate(errors):
            f.write("{0},{1}\n".format(i+1, error))

def parse_properties():
    with open("config.json") as json_file:
        json_values = json.load(json_file)
    

    neurons_per_layer = get_hidden_layer_neurons(json_values.get("neurons_per_layer"), json_values.get("latent_layer_neurons"))
    
    font = json_values.get("font_set")
    font_chars = get_font_characters(font)
    font_subset_size = json_values.get("font_subset_size")
    training_set = get_training_set(font, font_subset_size)
    orig_training_set = training_set
    output_set = training_set
    noise_prob = 0
    mode = json_values.get("mode")
    if (mode == "DAE"):
        orig_training_set = training_set.copy()
        orig_output_set = output_set.copy()
        noise_prob = json_values.get("noise_probability")
        training_set = noise_font(orig_training_set, noise_prob)
        for i in range(4):
            output_set += orig_output_set
            training_set += noise_font(orig_training_set, noise_prob)

    beta = json_values.get("beta")
    if beta == None or beta <= 0:
        print("Positive beta required")
        exit(-1)
    Properties.beta = beta

    epochs = json_values.get("epochs")
    if epochs == None or epochs <= 0:
        print("Positive epochs required")
        exit(-1)
      
    return Properties(neurons_per_layer,font,font_chars,epochs,training_set,output_set,mode,noise_prob,orig_training_set)

# Assembles a decoder with the given neurons_per_layer, a latent layer with the given latent_layer_neurons, and a decoder reversing the encoder.
def get_hidden_layer_neurons(neurons_per_layer, latent_layer_neurons):
    if neurons_per_layer == None or latent_layer_neurons == None:
        return None
    if len(neurons_per_layer) < 0 or latent_layer_neurons <= 0:
        return None
    
    hidden_layer_neurons = neurons_per_layer.copy()
    hidden_layer_neurons.append(latent_layer_neurons)
    for neurons in reversed(neurons_per_layer):
        hidden_layer_neurons.append(neurons)

    return hidden_layer_neurons

# Sets the training set of the given properties to the given font set
def get_training_set(font_set, font_subset_size=None):
    if font_set == None:
        return None
    if font_set not in fonts.font_sets:
        return None
    
    training_set = []
    font_set = fonts.font_sets.get(font_set)
    for letter in font_set:
        binary_array = fonts.font_char_to_bin_arr(letter)
        training_set.append(binary_array)


    if font_subset_size != None and font_subset_size < len(training_set):
        training_set = training_set[:font_subset_size]

    return training_set

def get_font_characters(font_set):
    return fonts.font_names.get(font_set)




    
