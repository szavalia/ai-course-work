from models import Observables, Properties, VAEObservables
from io_parser import parse_properties,generate_output
import algorithms.autoencoder as autoencoder
import algorithms.vae as vae
def __main__():

    #Parse parameters
    properties:Properties = parse_properties()

    if(properties.mode != "VAE"):
        observables:Observables =  autoencoder.execute(properties)
        generate_output(properties,observables)
    else:
        observables:VAEObservables = vae.execute(properties)
        print(len(observables.latent_outputs))
        print(len(observables.colors))
        

if __name__ == "__main__":
    __main__()