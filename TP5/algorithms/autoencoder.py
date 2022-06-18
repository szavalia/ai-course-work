from models import Autoencoder, Observables, Properties
import numpy as np
import scipy.optimize as sco

def execute(properties:Properties):
    # Create autoencoder
    autoencoder:Autoencoder = build_autoencoder(properties)

    # Train
    trained_weigths = train_autoencoder(autoencoder,properties)

    print("\nTrained weights:\n\n" + str(trained_weigths))

    print(autoencoder.error(trained_weigths))

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
