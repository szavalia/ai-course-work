from models import Observables, Properties
from io_parser import parse_properties,generate_output
from algorithms.autoencoder import execute
def __main__():

    #Parse parameters
    properties:Properties = parse_properties()

    observables:Observables =  execute(properties)

    generate_output(properties,observables)
        

if __name__ == "__main__":
    __main__()