import numpy as np
#The parameters for the running of perceptron
class Perceptron:
    def __init__(self,type,learning_rate,max_epochs,min_error,problem,function,sigmoid_type=None,dfunction=None,neurons_per_layer=None):
        self.type = type
        self.max_epochs = max_epochs
        self.min_error = min_error 
        self.problem = problem
        self.function = function
        self.learning_rate = learning_rate
        self.sigmoid_type = sigmoid_type
        self.d_function = dfunction
        self.neurons_per_layer = neurons_per_layer

class Properties:
    beta = 0
    softmax = False 
    def __init__(self,perceptron:Perceptron,training_set,output_set,normalized_function, metrics_function,cross_validate,test_proportion):
        self.perceptron = perceptron
        self.training_set = training_set
        self.output_set = output_set
        self.normalized_function = normalized_function
        self.metrics_function = metrics_function
        self.cross_validate = cross_validate
        self.test_proportion = test_proportion
        self.output_max = 0
        self.output_min = 0
        self.sigmoid_max = 0
        self.sigmoid_min = 0

class Neuron:
    function = None
    d_function = None
    
    def __init__(self, w, learning_rate):
        self.w = w
        self.learning_rate = learning_rate
        self.excitement = 0
        self.previous_inc = None
        
    def get_activation(self, entry):
        self.excitement = np.dot(self.w, entry)
        return Neuron.function(self.excitement)
        
    # Calculates the error for a neuron in the output layer using the expected_output and the neuron's activation value
    def calculate_output_delta(self,expected_output,activation):
        return Neuron.d_function(self.excitement)*(expected_output-activation)
        
    # Calculates the error for a neuron in a hidden layer using the error of a superior layer
    def calculate_delta(self, superior_delta,w_aux):
        return (Neuron.d_function(self.excitement) * np.dot(w_aux,superior_delta))
    
    def update_w(self,delta,activations):
        increments = []
        for activation in activations:
            increments.append(self.learning_rate*activation*delta)
        self.w += increments
        if(Properties.alpha > 0):
            if (self.previous_inc is not None):
                self.w += Properties.alpha * self.previous_inc
            self.previous_inc = np.array(increments)

class ThresholdNeuron:

    def get_activation(self,entry):
        return -1


class Layer:
    def __init__(self, neurons):
        self.neurons = neurons
    
    def get_activations(self, entry):
        activations = []
        for neuron in self.neurons:
            activations.append(neuron.get_activation(entry))
        return activations
    
    # Returns the deltas for the neurons
    def get_deltas(self, superior_error,superior_layer=None,activations=None,isBelowOutput=False,properties:Properties=None):
        deltas = []
        superior_weights = []
        if(superior_layer != None):
            if (isBelowOutput):
                for neuron in superior_layer.neurons[:]:
                    superior_weights.append(neuron.w)
            else:
                for neuron in superior_layer.neurons[1:]:
                    superior_weights.append(neuron.w)
        for (idx,neuron) in enumerate(self.neurons):
            if(activations != None):
                # If the activation value is set, it means that it's an output layer
                deltas.append(neuron.calculate_output_delta(properties.normalized_function(properties.output_max,properties.output_min,properties.sigmoid_max,properties.sigmoid_min,superior_error[idx]),activations[idx]))
            else:
                if(idx != 0):
                    w_aux = []
                    for w in superior_weights:
                        w_aux.append(w[idx])
                    deltas.append(neuron.calculate_delta(superior_error,w_aux))
        return deltas

    def update_neurons(self,deltas,activations,isOutput):
        for (idx,neuron) in enumerate(self.neurons):
            if(idx == 0 and not isOutput):
                continue
            if isOutput:
                neuron.update_w(deltas[idx],activations)
            else:
                neuron.update_w(deltas[idx-1],activations)

class Observables:
    def __init__(self,w,training_error,epochs,metrics=None):
        self.w = w
        self.training_error = training_error
        self.epochs = epochs
        self.metrics = metrics
        self.test_error = 0

# Metrics for a given class
class Metrics:
    def __init__(self,accuracy,precision=None,recall=None,f1_score=None,true_positive_rate=None,false_positive_rate=None,studied_class=None):
        self.accuracy=accuracy
        self.precision=precision
        self.recall=recall
        self.f1_score=f1_score
        self.true_positive_rate=true_positive_rate
        self.false_positive_rate=false_positive_rate
