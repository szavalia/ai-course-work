from models import Properties
from io_parser import parse_properties
from algorithms.autoencoder import execute
def __main__():

    #Parse parameters
    properties:Properties = parse_properties()

    execute(properties)
        

if __name__ == "__main__":
    __main__()