import numpy as np

class HopfieldProperties:
    def __init__(self,letters,patterns,noise_prob, noise_patterns):
        self.method = "hopfield"
        self.letters = letters
        self.patterns = patterns
        self.noise_patterns = noise_patterns
        self.noise_prob = noise_prob

class HopfieldObservables:
    def __init__(self,pattern_states):
        self.pattern_states = pattern_states

class KohonenProperties:
    def __init__(self,input_names,input_set,eta,k,r,epochs):
        self.method = "kohonen"
        self.input_names = input_names
        self.input_set = input_set
        self.eta = eta
        self.k = k
        self.r = r
        self.epochs = epochs
    
class KohonenObservables:
    def __init__(self,classifications,u_matrix):
        self.classifications = classifications
        self.u_matrix = u_matrix

class KohonenNeuron:
    def __init__(self,w,i,j):
        self.w = w
        self.i = i
        self.j = j
    
    def update_w(self,xp,eta):
        self.w += eta * (np.array(xp) - np.array(self.w))

class OjaProperties:
    def __init__(self,input_names,input_set,eta,epochs):
        self.method = "oja"
        self.input_names = input_names
        self.input_set = input_set
        self.eta = eta
        self.epochs = epochs

class OjaObservables:
    def __init__(self,principal_component, loadings):
        self.principal_component = principal_component
        self.loadings = loadings
