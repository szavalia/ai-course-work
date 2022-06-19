from models import Autoencoder, Observables, Properties
import numpy as np
import scipy.optimize as sco
from algorithms.noiser import noise_font

def execute(properties:Properties):
    # Create autoencoder
    autoencoder:Autoencoder = build_autoencoder(properties)

    # Train
    trained_weigths = train_autoencoder(autoencoder,properties)

    print("\nTrained weights:\n\n" + str(trained_weigths))

    print("Final error: " + str(autoencoder.error(trained_weigths)))
    
    # After training: 
    # Get outputs for inputs
    unflattened = autoencoder.unflatten_weights(trained_weigths)
    output = []
    for letter in properties.training_set:
        output.append(autoencoder.get_output(letter,unflattened))

    # If mode was DAE, get new noised font and see how well it denoises
    if properties.mode == "DAE":
        noised_font = noise_font(properties.orig_training_set, properties.noise_prob)
        noised_output = []
        for letter in noised_font:
            noised_output.append(autoencoder.get_output(letter,unflattened))
        # print error for noised font
        print("\nError for new noised font: " + str(autoencoder.error_given_sets(trained_weigths, noised_font)))

    f = open("outputs.csv", "w")
    f.write("Calculated,Letter,Row,Column,Value\n")
    for (k,letter) in enumerate(properties.training_set):
        for i in range(7):
            for j in range(5):
                f.write(str(0) + "," + str(k) + "," + str(i) + "," + str(j) + "," + str(letter[i*5+j]) + "\n")
    for (k,letter) in enumerate(output):
        for i in range(7):
            for j in range(5):
                f.write(str(1) + "," + str(k) + "," + str(i) + "," + str(j) + "," + str(letter[i*5+j]) + "\n")
    if properties.mode == "DAE":
        for (k,letter) in enumerate(noised_font):
            for i in range(7):
                for j in range(5):
                    f.write(str(2) + "," + str(k) + "," + str(i) + "," + str(j) + "," + str(letter[i*5+j]) + "\n")
        for (k,letter) in enumerate(noised_output):
            for i in range(7):
                for j in range(5):
                    f.write(str(3) + "," + str(k) + "," + str(i) + "," + str(j) + "," + str(letter[i*5+j]) + "\n")
    f.close()

    autoencoder.weights = autoencoder.unflatten_weights(trained_weigths)

    latent_outputs = get_latent_outputs(autoencoder)

    return Observables(autoencoder.errors_per_step,latent_outputs)

def build_autoencoder(properties:Properties):
    weights = []
    
    # Add layers
    for layer_index, neurons_count in enumerate(properties.neurons_per_layer):
        weights.append([])  
        for index in range(0, neurons_count):
            if layer_index == 0: 
                w = np.random.randn(len(properties.training_set[0]))
            else:
                w = np.random.randn(len(weights[-2]))
            weights[-1].append(w)

    # Add output layer of decoder
    # Number of neurons in output layer depends on number of camps in expected output values
    weights.append([])
    for i in range(len(properties.output_set[0])):
        w = np.random.randn(len(weights[-2]))
        weights[-1].append(w)
    
    # Convert to ndarray
    for (i, layer) in enumerate(weights):
        weights[i] = np.array(layer, dtype=float)

    return Autoencoder(np.array(weights, dtype=object),int((len(properties.neurons_per_layer))/2),properties.training_set,properties.output_set,properties.neurons_per_layer)

def flatten_weights(weigths):
    flattened_weights = np.array([])
    for (i,layer) in enumerate(weigths):
        flattened_weights =  np.append(flattened_weights,layer.flatten())
    return flattened_weights.flatten() 
    
def train_autoencoder(autoencoder:Autoencoder,properties:Properties):
    flattened_weights = flatten_weights(autoencoder.weights)

    trained_weights = sco.minimize(
            autoencoder.error, flattened_weights, method='Powell', callback=autoencoder.callback, 
            options={'maxiter': properties.epochs}
        ).x

    return trained_weights

def get_latent_outputs(autoencoder:Autoencoder):
    outputs = []
    for input in autoencoder.training_set:
        outputs.append(autoencoder.get_latent_output(input))
    return outputs
