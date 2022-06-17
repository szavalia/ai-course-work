import json
import numpy as np
from models import Properties
import fonts
from algorithms.noiser import noise_font

def parse_properties():
    with open("config.json") as json_file:
        json_values = json.load(json_file)
    

    neurons_per_layer = get_hidden_layer_neurons(json_values.get("neurons_per_layer"), json_values.get("latent_layer_neurons"))
    
    font = json_values.get("font_set")
    training_set = get_training_set(font)
    output_set = training_set
    if (json_values.get("mode") == "DAE"):
        training_set = noise_font(training_set, json_values.get("noise_probability"))

    learning_rate = json_values.get("learning_rate")
    if learning_rate == None or learning_rate <= 0:
        print("Positive learning rate required")
        exit(-1)

    beta = json_values.get("beta")
    if beta == None or beta <= 0:
        print("Positive beta required")
        exit(-1)
    Properties.beta = beta

    epochs = json_values.get("epochs")
    if epochs == None or epochs <= 0:
        print("Positive epochs required")
        exit(-1)
      
    return Properties(neurons_per_layer,font,learning_rate,epochs,training_set,output_set)

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
def get_training_set(font_set):
    if font_set == None:
        return None
    if font_set not in fonts.font_sets:
        return None
    
    training_set = []
    font_set = fonts.font_sets.get(font_set)
    for letter in font_set:
        binary_array = fonts.font_char_to_bin_arr(letter)
        training_set.append(binary_array)

    return training_set




    
