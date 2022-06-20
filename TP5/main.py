from models import Observables, Properties, VAEObservables
from io_parser import parse_properties,generate_output,generate_VAE_output
import algorithms.autoencoder as autoencoder
import algorithms.vae as vae
def __main__():

    #Parse parameters
    properties:Properties = parse_properties()

    if(properties.mode == "DEFAULT" or properties.mode == "DAE"):
        observables:Observables =  autoencoder.execute(properties)
        generate_output(properties,observables)
    elif(properties.mode == "VAE"):
        observables:VAEObservables = vae.execute(properties)
        generate_VAE_output(properties,observables)
        

if __name__ == "__main__":
    __main__()