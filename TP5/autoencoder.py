from models import Autoencoder, Properties
#import tensorflow as tf
#from tensorflow.keras.optimizers import Adam
import numpy as np
import numdifftools as nd
from autograd.misc.optimizers import adam

def execute(properties:Properties):
    # Create autoencoder
    autoencoder:Autoencoder = build_autoencoder(properties)

    # Train
    trained_weigths = train_autoencoder(autoencoder,properties)

    print("\nTrained weights:\n\n" + str(trained_weigths))

def train_autoencoder(autoencoder:Autoencoder,properties:Properties):
    flattened_weights = np.array([])
    for (i,layer) in enumerate(autoencoder.weights):
        flattened_weights =  np.append(flattened_weights,layer.flatten())
    flattened_weights = flattened_weights.flatten()
    print("\nEpochs: " + str(properties.epochs))
    trained_weights = adam(nd.Gradient(autoencoder.error),flattened_weights,callback=None,num_iters=properties.epochs,step_size=0.001, b1=0.9, b2=0.999, eps=10**-8) 
    return trained_weights

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

    return Autoencoder(np.array(weights, dtype=object),(len(properties.neurons_per_layer) + 1)/ 2,properties.training_set,properties.output_set,properties.neurons_per_layer)
