import json
import numpy as np
from models import Properties
import fonts

def parse_properties(path_to_json):
    with open(path_to_json) as json_file:
        json_values = json.load(json_file)
    
    
    properties = Properties()
    #TODO: Add "mode" field to config.json

    set_hidden_layer_neurons(properties, json_values.get("neurons_per_layer"), json_values.get("latent_layer_neurons"))
    
    set_training_set(properties, json_values.get("font_set"))

    learning_rate = json_values.get("learning_rate")
    if learning_rate == None or learning_rate <= 0:
        print("Positive learning rate required")
        exit(-1)
    properties.learning_rate = learning_rate

    beta = json_values.get("beta")
    if beta == None or beta <= 0:
        print("Positive beta required")
        exit(-1)
    properties.beta = beta

    epochs = json_values.get("epochs")
    if epochs == None or epochs <= 0:
        print("Positive epochs required")
        exit(-1)
    properties.epochs = epochs
      
    return properties

# Assembles a decoder with the given neurons_per_layer, a latent layer with the given latent_layer_neurons, and a decoder reversing the encoder.
def set_hidden_layer_neurons(properties:Properties, neurons_per_layer, latent_layer_neurons):
    if neurons_per_layer == None or latent_layer_neurons == None:
        return None
    if len(neurons_per_layer) <= 0 or latent_layer_neurons <= 0:
        return None
    
    hidden_layer_neurons = neurons_per_layer.copy()
    hidden_layer_neurons.append(latent_layer_neurons)
    for neurons in reversed(neurons_per_layer):
        hidden_layer_neurons.append(neurons)

    properties.neurons_per_layer = hidden_layer_neurons

# Sets the training set of the given properties to the given font set
def set_training_set(properties:Properties, font_set):
    if font_set == None:
        return None
    if font_set not in fonts.font_sets:
        return None
    
    training_set = []
    font_set = fonts.font_sets[font_set]
    for letter in font_set:
        binary_array = fonts.font_char_to_bin_arr(letter)
        training_set.append(binary_array)
    
    properties.training_set = training_set
    properties.output_set = training_set

    #TODO: if "mode" is "DAE", add noise to the training set and set the original as output set



    
