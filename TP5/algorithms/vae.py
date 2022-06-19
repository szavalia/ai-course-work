from models import Properties, VAEObservables
from keras.layers import Input, Dense, Lambda, Reshape
from keras.models import Model
from keras import backend as K
from keras import metrics
import tensorflow as tf
import numpy as np
from keras.datasets import mnist

from tensorflow.python.framework.ops import disable_eager_execution
disable_eager_execution()

def execute(properties:Properties):
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_train = x_train.astype('float32') / 255.
    x_test = x_test.astype('float32') / 255.
    x_train = x_train.reshape((len(x_train), np.prod(x_train.shape[1:])))
    x_test = x_test.reshape((len(x_test), np.prod(x_test.shape[1:])))
    vae = VAE(2,28*28,[256])
    vae.train(x_train,properties.epochs,100)
    latent_outputs = vae.encoder.predict(x_test, batch_size=len(properties.training_set))[0]
    return VAEObservables(latent_outputs,y_test)

def flatten_set(training_set):
    return np.array(training_set).reshape((len(training_set), np.prod(np.array(training_set).shape[1:])))
    
class VAE:
    def __init__(self,latent_neurons,dim,intermediate_layers):
        self.latent_neurons = latent_neurons
        self.dim = dim
        self.intermediate_layers = intermediate_layers
        self.set_vae()

    def train(self,training_set,epochs,batch_size):
        self.model.fit(training_set,training_set,epochs=epochs)
    
    def set_vae(self):
        # input to our encoder
        x = Input(shape=(self.dim,), name="input")
        self.encoder = self.set_encoder(x)
        # print out summary of what we just did
        self.encoder.summary()
        self.decoder = self.set_decoder()
        self.decoder.summary()
        # grab the output. Recall, that we need to grab the 3rd element our sampling z
        output_combined = self.decoder(self.encoder(x)[2])
        # link the input and the overall output
        self.model = Model(x, output_combined)
        # print out what the overall model looks like
        self.model.summary()
        self.model.compile(loss=self.vae_loss)
        
    def set_encoder(self,x):
        # intermediate layers
        if(len(self.intermediate_layers) != 0):
            aux_h = x
            for (i,neurons) in enumerate(self.intermediate_layers[:-1]):
                h = Dense(neurons, name="encoding_{0}".format(i))(aux_h)
                aux_h = h
            h = Dense(self.intermediate_layers[-1],activation='relu', name="encoding_{0}".format(len(self.intermediate_layers)-1))(aux_h)
        # defining the mean of the latent space
        self.z_mean = Dense(self.latent_neurons, name="mean")(h)
        # defining the log variance of the latent space
        self.z_log_var = Dense(self.latent_neurons, name="log-variance")(h)
        # note that "output_shape" isn't necessary with the TensorFlow backend
        z = Lambda(self.get_samples, output_shape=(self.latent_neurons,))([self.z_mean, self.z_log_var])
        # defining the encoder as a keras model
        encoder = Model(x, [self.z_mean, self.z_log_var, z], name="encoder")
        return encoder
    
    def set_decoder(self):
        # Input to the decoder
        input_decoder = Input(shape=(self.latent_neurons,), name="decoder_input")
        # intermediate layers
        reversed_layers = self.intermediate_layers.copy()
        reversed_layers.reverse()
        if(len(self.intermediate_layers) != 0):
            aux_h = input_decoder
            for (i,neurons) in enumerate(reversed_layers[:-1]):
                h = Dense(neurons, name="encoding_{0}".format(i))(aux_h)
                aux_h = h
            h = Dense(reversed_layers[-1],activation='relu', name="encoding_{0}".format(len(self.intermediate_layers)-1))(aux_h)
        #getting the mean from the original dimension
        x_decoded = Dense(self.dim, activation='sigmoid', name="flat_decoded")(h)
        # defining the decoder as a keras model
        decoder = Model(input_decoder, x_decoded, name="decoder")
        return decoder

    def get_samples(self,args: tuple):
        # we grab the variables from the tuple
        z_mean, z_log_var = args
        print(z_mean)
        print(z_log_var)
        epsilon = K.random_normal(shape=(K.shape(z_mean)[0], self.latent_neurons), mean=0.,stddev=1.0)
        return z_mean + K.exp(z_log_var / 2) * epsilon  # h(z)
    
    def vae_loss(self,x: tf.Tensor, x_decoded_mean: tf.Tensor):
        # Aca se computa la cross entropy entre los "labels" x que son los valores 0/1 de los pixeles, y lo que salió al final del Decoder.
        xent_loss = self.dim * metrics.binary_crossentropy(x, x_decoded_mean) # x-^X
        kl_loss = - 0.5 * K.sum(1 + self.z_log_var - K.square(self.z_mean) - K.exp(self.z_log_var), axis=-1)
        vae_loss = K.mean(xent_loss + kl_loss)
        return vae_loss