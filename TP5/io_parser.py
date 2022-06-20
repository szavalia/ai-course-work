import json
import numpy as np
from models import Properties,Observables, VAEObservables
import fonts
from algorithms.noiser import noise_font

def generate_output(properties:Properties, observables:Observables):
    print("Mode: {0}".format(properties.mode))
    print("Neurons per layer: {0}".format(properties.neurons_per_layer))
    print("Font: {0}".format(properties.font))
    print("Epochs: {0}".format(properties.epochs))
    generate_latent_outputs(observables.latent_outputs,properties.font_chars)
    generate_errors_output(observables.errors_per_step)

def generate_output_file(mode,training_set,output,noised_font,noised_output):
    f = open("outputs.csv", "w")
    f.write("Calculated,Letter,Row,Column,Value\n")
    for (k,letter) in enumerate(training_set):
        for i in range(7):
            for j in range(5):
                f.write(str(0) + "," + str(k) + "," + str(i) + "," + str(j) + "," + str(letter[i*5+j]) + "\n")
    for (k,letter) in enumerate(output):
        for i in range(7):
            for j in range(5):
                f.write(str(1) + "," + str(k) + "," + str(i) + "," + str(j) + "," + str(letter[i*5+j]) + "\n")
    if mode == "DAE":
        for (k,letter) in enumerate(noised_font):
            for i in range(7):
                for j in range(5):
                    f.write(str(2) + "," + str(k) + "," + str(i) + "," + str(j) + "," + str(letter[i*5+j]) + "\n")
        for (k,letter) in enumerate(noised_output):
            for i in range(7):
                for j in range(5):
                    f.write(str(3) + "," + str(k) + "," + str(i) + "," + str(j) + "," + str(letter[i*5+j]) + "\n")
    f.close()

def generate_samples_file(char_pairs,samples):
    f = open("samples.csv", "w")
    f.write("Char1,Char2,Sample,Row,Column,Value\n")
    for (h,char_pair) in enumerate(char_pairs):
        for (k,sample) in enumerate(samples[h]):
            for i in range(7):
                for j in range(5):
                    f.write("{0},{1},{2},{3},{4},{5}\n".format(char_pair[0], char_pair[1], k, i, j,sample[i*5+j]))
    f.close()        


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

def generate_VAE_output(properties:Properties,observables:VAEObservables):
    print("Mode: {0}".format(properties.mode))
    print("Neurons per layer: {0}".format(properties.neurons_per_layer))
    print("Epochs: {0}".format(properties.epochs))
    generate_VAE_latent_outputs(observables)

def generate_VAE_latent_outputs(observables:VAEObservables):
   with open("VAE_latent.csv", "w") as f:
        f.write("X,Y,Value\n")
        for (i,output) in enumerate(observables.latent_outputs):
            f.write("{0},{1},{2}\n".format(output[0], output[1],observables.colors[i]))

def parse_properties():
    with open("config.json") as json_file:
        json_values = json.load(json_file)
    

    neurons_per_layer = get_hidden_layer_neurons(json_values.get("neurons_per_layer"), json_values.get("latent_layer_neurons"))
    
    training_set = None
    font = None
    font_chars = None
    output_set = None
    noise_prob = 0
    orig_training_set = None
    mode = json_values.get("mode")
    if(mode == "DAE" or mode == "DEFAULT"):
        beta = json_values.get("beta")
        if beta == None or beta <= 0:
            print("Positive beta required")
            exit(-1)
        Properties.beta = beta
        font = json_values.get("font_set")
        font_chars = get_font_characters(font)
        font_subset_size = json_values.get("font_subset_size")
        training_set = get_training_set(font, font_subset_size)
        orig_training_set = training_set
        output_set = training_set
        noise_prob = 0
        if (mode == "DAE"):
            orig_training_set = training_set.copy()
            orig_output_set = output_set.copy()
            noise_prob = json_values.get("noise_probability")
            training_set = noise_font(orig_training_set, noise_prob)
            for i in range(4):
                output_set += orig_output_set
                training_set += noise_font(orig_training_set, noise_prob)

    epochs = json_values.get("epochs")
    if epochs == None or epochs <= 0:
        print("Positive epochs required")
        exit(-1)

    dataset = None
    if(mode == "VAE"):
        dataset = json_values.get("vae_dataset")
        if(dataset == None or dataset != "mnist" or dataset != "fashion_mnist"):
            print("Valid dataset for VAE required")
            exit(-1)
      
    return Properties(neurons_per_layer,font,font_chars,epochs,training_set,output_set,mode,noise_prob,orig_training_set,dataset)

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




    
