from models import Autoencoder, Observables, Properties
import numpy as np
import scipy.optimize as sco
from algorithms.noiser import noise_font
from io_parser import generate_output_file,generate_samples_file
from autograd.misc.optimizers import adam 
import numdifftools as nd 

def execute(properties:Properties):
    # Create autoencoder
    autoencoder:Autoencoder = build_autoencoder(properties)

    # Train
    trained_weigths = train_autoencoder(autoencoder,properties)

    autoencoder.weights = autoencoder.unflatten_weights(trained_weigths)
    
    # After training: 
    # Get outputs for inputs
    unflattened = autoencoder.unflatten_weights(trained_weigths)
    output = autoencoder.get_output(properties.training_set, unflattened)

    # If mode was DAE, get new noised font and see how well it denoises
    noised_font = None
    noised_output = None
    if properties.mode == "DAE":
        noised_font = noise_font(properties.orig_training_set, properties.noise_prob)
        noised_output = []
        for letter in noised_font:
            noised_output.append(autoencoder.get_output(letter,unflattened))
        # print error for noised font
        print("\nError for new noised font: " + str(autoencoder.error_given_sets(trained_weigths, noised_font)))

    generate_output_file(properties.mode,properties.training_set,output,noise_font,noised_output)
    latent_outputs = get_latent_outputs(autoencoder,properties)

    if properties.mode == "DEFAULT" and properties.neurons_per_layer[autoencoder.latent_index] == 2:
        distances = get_distances(latent_outputs)
        pairs = [distances[0][:2],distances[int(len(distances)/2)][:2],distances[-1][:2]]

        samples = []
        char_pairs = []
        for pair_indexes in pairs:
            value1 = latent_outputs[pair_indexes[0]]
            value2 = latent_outputs[pair_indexes[1]]
            char_pairs.append([properties.font_chars[pair_indexes[0]],properties.font_chars[pair_indexes[1]]])
            samples.append(get_samples(value1,value2,autoencoder))
        
        generate_samples_file(char_pairs,samples)

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

    # Optimize
    if properties.minimizer == "powell":
        trained_weights = sco.minimize(
                autoencoder.error, flattened_weights, method='Powell', callback=autoencoder.callback, 
                options={'maxiter': properties.epochs}
            ).x
    elif properties.minimizer == "adam":
        trained_weights = adam(nd.Gradient(autoencoder.error), flattened_weights, callback=autoencoder.callback, num_iters=properties.epochs, step_size=0.1, b1=0.9, b2=0.999, eps=10**-2)    

    return trained_weights

def get_latent_outputs(autoencoder:Autoencoder,properties:Properties):
    return autoencoder.get_latent_output(properties.training_set)

def get_decoder_outputs(autoencoder:Autoencoder,samples):
    return autoencoder.get_decoder_output(samples)

def get_distances(points):
    distances = []
    for (i,value) in enumerate(points):
        for j in range(i+1, len(points)):
            distances.append(np.array([int(i),int(j),np.linalg.norm(value - points[j])], dtype = object))
    distances = np.array(distances, dtype = object)
    return distances[distances[:, 2].argsort()]

def line(m,b,x):
    return m*x - b

def get_samples(point1,point2,autoencoder:Autoencoder):
    m = (point1[1]-point2[1]) / (point1[0]-point2[0])
    b = (point1[0]*point2[1] - point2[0]*point1[1])/(point1[0]-point2[0])

    min_x = min(point1[0],point2[0])
    max_x = max(point1[0],point2[0])
    inputs = []

    print(np.linspace(min_x,max_x,5))
    for x in np.linspace(min_x,max_x,5):
        y = line(m,b,x)
        inputs.append(np.array([x,y]))
    
    inputs = np.array(inputs)

    #print(inputs)

    outputs = autoencoder.get_decoder_output(inputs)

    return outputs




