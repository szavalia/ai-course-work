class Properties:
    def __init__(self,neurons_per_layer,font,learning_rate,beta,error_threshold,epochs):
        self.neurons_per_layer = neurons_per_layer
        self.font = font
        self.learning_rate = learning_rate
        self.beta = beta
        self.epochs = epochs
        self.training_set = []
        self.output_set = []
    
    def __init__(self):
        pass    