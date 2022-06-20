import numpy as np
import scipy.optimize as sco
import warnings
warnings.filterwarnings(action='ignore', category=RuntimeWarning)

class Properties:
    beta = 0
    def __init__(self,neurons_per_layer,font,font_chars,epochs,training_set,output_set,mode,noise_prob,orig_training_set,VAE_dataset):
        self.neurons_per_layer = neurons_per_layer
        self.font = font
        self.font_chars = font_chars
        self.epochs = epochs
        self.training_set = training_set
        self.output_set = output_set
        self.mode = mode
        self.noise_prob = noise_prob
        self.orig_training_set = orig_training_set
        self.VAE_dataset = VAE_dataset
    
class Observables:
    def __init__(self,errors_per_step,latent_outputs):
        self.errors_per_step = errors_per_step
        self.latent_outputs = latent_outputs

class VAEObservables:
    def __init__(self,latent_outputs,colors):
        self.latent_outputs = latent_outputs
        self.colors = colors
    
class Autoencoder:
    def __init__(self,weights,latent_index,training_set,output_set,neurons_per_layer):
        self.weights = weights
        self.latent_index = latent_index
        self.training_set = training_set
        self.output_set = output_set
        self.neurons_per_layer = neurons_per_layer
        self.curr_epoch = 0
        self.functions = []
        self.set_functions()
        self.errors_per_step = []
    
    def set_functions(self):
        for i in range(0,len(self.weights)):
            if i <= self.latent_index:
                self.functions.append(self.linear)
            else:
                self.functions.append(self.logistic)

    def callback(self,x):
        self.errors_per_step.append(self.error(x))
        self.curr_epoch += 1
        print("Epoch: {1}. Error: {0}".format(self.errors_per_step[-1], self.curr_epoch))

    def relu(self,x):
        return np.where(x <= 0, 0, x)
    
    def logistic(self,x):
        return  1 / (1 + np.exp(-2*Properties.beta * x))

    def linear(self,x):
        return x

    def get_output(self, input, weights):
        for (i,layer) in enumerate(weights):
            h = np.dot(input, layer.T)
            # Transform dot products into activations
            input = self.functions[i](h)
        
        # Return results of last layer (network outputs)
        return input

    def get_latent_output(self,input):
        for(i,layer) in enumerate(self.weights[:self.latent_index+1]):
            h = np.dot(input, layer.T)

            # Transform dot products into activations
            input = self.functions[i](h)
        
        # Return results of latent layer
        return input

    def get_decoder_output(self,input):
        for(i,layer) in enumerate(self.weights[self.latent_index+1:]):
            h = np.dot(input, layer.T)

            # Transform dot products into activations
            input = self.functions[i+self.latent_index+1](h)
        
        # Return results of latent layer
        return input

    def error(self, weights):
        error = 0
        unflattened_weights = self.unflatten_weights(weights)
        expected = np.array(self.output_set)
        output = self.get_output(self.training_set,unflattened_weights)
        error = np.sum(np.power(output-expected,2)) 
                      
        return error*(1/2)


    # For DAE where we need to pass new noised data
    def error_given_sets(self, weights, input_set):
        error = 0
        unflattened_weights = self.unflatten_weights(weights)
        for (i,entry) in enumerate(input_set):
            expected = np.array(self.output_set[i])
            output = np.array(self.get_output(entry, unflattened_weights))

            for (idx,output_value) in enumerate(output):
                error += (output_value - expected[idx])**2
                      
        return error*(1/2)

    # Converts from 1D array back to 3D structure
    def unflatten_weights(self, array):
        new_arr = []
        i = 0
        for layer in self.weights:
            curr_size = layer.size
            flatted = np.array(array[i:i+curr_size])
            new_arr.append(flatted.reshape(layer.shape))
            i += curr_size
        new_arr = np.array(new_arr, dtype=object)
        return new_arr
